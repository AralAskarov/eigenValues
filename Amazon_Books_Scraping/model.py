import pandas as pd
import numpy as np
from fuzzywuzzy import process
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import OneHotEncoder
from fastapi import FastAPI, HTTPException, Depends
import requests
from pydantic import BaseModel
from typing import List, Dict, Any
from collections import defaultdict



class ServiceAPI:
    def __init__(self, base_url: str):
        self.base_url = base_url 
    def get_user_preferences(self, user_id: int) -> Dict[str, Any]:
        response = requests.get(f"{self.base_url}/user/{user_id}/preferences")
        try:
            response = requests.get(f"{self.base_url}/user/{user_id}/preferences")
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 404:
                # Return empty preferences if not found
                return {"Main Genre": {}, "Sub Genre": {}, "Type": {}, "Author": {}}
            else:
                print(f"Error getting user preferences: {response.status_code}")
                return {"Main Genre": {}, "Sub Genre": {}, "Type": {}, "Author": {}}
        except Exception as e:
            print(f"Exception getting user preferences: {str(e)}")
            return {"Main Genre": {}, "Sub Genre": {}, "Type": {}, "Author": {}}
        
    def update_user_preferences(self, user_id: int, preferences: dict):
        try:
            response = requests.post(f"{self.base_url}/user/{user_id}/preferences", json=preferences)
            if response.status_code != 200:
                print(f"Error updating user preferences: {response.status_code}")
        except Exception as e:
            print(f"Exception updating user preferences: {str(e)}")

    def update_global_preferences(self, preferences: dict):
        try:
            response = requests.post(f"{self.base_url}/global/preferences", json=preferences)
            if response.status_code != 200:
                print(f"Error updating user preferences: {response.status_code}")
        except Exception as e:
            print(f"Exception updating user preferences: {str(e)}")

    def get_global_preferences(self) -> Dict[str, Any]:
        # Instead of failing, provide default global preferences
        try:
            response = requests.get(f"{self.base_url}/global/preferences")
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Error getting global preferences: {response.status_code}")
                # Return default global preferences
                return {
                    "Main Genre": {"Fiction": 0.5, "Non-Fiction": 0.5},
                    "Sub Genre": {"Fantasy": 0.5, "SciFi": 0.5, "Mystery": 0.5, "Romance": 0.5, "Biography": 0.5},
                    "Type": {"Paperback": 0.5, "Hardcover": 0.5, "eBook": 0.5},
                    "Author": {}  # Empty default for authors
                }
        except Exception as e:
            print(f"Exception getting global preferences: {str(e)}")
            # Return default global preferences
            return {
                "Main Genre": {"Fiction": 0.5, "Non-Fiction": 0.5},
                "Sub Genre": {"Fantasy": 0.5, "SciFi": 0.5, "Mystery": 0.5, "Romance": 0.5, "Biography": 0.5},
                "Type": {"Paperback": 0.5, "Hardcover": 0.5, "eBook": 0.5},
                "Author": {}  # Empty default for authors
            }
    
    def get_all_user_preferences(self) -> Dict[int, Dict[str, Any]]:
        """
        Получить предпочтения всех пользователей.
        Возвращает словарь, где ключ — user_id, значение — словарь предпочтений.
        """
        try:
            response = requests.get(f"{self.base_url}/users/preferences")
            if response.status_code == 200:
                return response.json()  # Ожидается формат: {user_id: {Category: {...}, ...}, ...}
            else:
                print(f"Error getting all user preferences: {response.status_code}")
                return {}
        except Exception as e:
            print(f"Exception getting all user preferences: {str(e)}")
            return {}

app = FastAPI()
class RecommendationRequest(BaseModel):
    user_id: int
    user_book_titles: List[str]
class RecommendationResponse(BaseModel):
    recommended_titles: List[str]

def get_db_service() -> ServiceAPI:
    return ServiceAPI(base_url="http://localhost:8000")

@app.post("/recommendations", response_model=RecommendationResponse)
def recommendations_endpoint(request: RecommendationRequest, db_api: ServiceAPI = Depends(get_db_service)):
    try:
        print(f"Processing request for user {request.user_id} with books: {request.user_book_titles}")
        result = compute_recommendations(request.user_id, request.user_book_titles, db_api)
        return RecommendationResponse(**result)
    except Exception as e:
        import traceback
        print(f"Error processing recommendation: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))

def collect_user_statistics(user_history, attributes):
    user_pref_sum = {attr: defaultdict(int) for attr in attributes}
    for book in user_history:
        for attr in attributes:
            value = book.get(attr)
            if value:
                user_pref_sum[attr][value] += 1
    user_count = len(user_history)
    return user_pref_sum, user_count

def bayesian_update(global_pref, user_pref_sum, user_count, prior_strength=1):
    updated_pref = {attr: {} for attr in global_pref}
    for attr in global_pref:
        for val in global_pref[attr]:
            prior = global_pref[attr][val]
            evidence = user_pref_sum[attr].get(val, 0)
            updated_pref[attr][val] = (prior_strength * prior + evidence) / (prior_strength + user_count)
    return updated_pref

def update_global_preferences(db_api: ServiceAPI, attributes: List[str]) -> Dict[str, Dict[str, float]]:
    """
    Вычисляет и обновляет глобальные предпочтения на основе средних значений
    предпочтений всех пользователей.

    Args:
        db_api: Экземпляр ServiceAPI для доступа к базе данных.
        attributes: Список атрибутов, по которым строятся предпочтения.

    Returns:
        Словарь с обновленными глобальными предпочтениями.
    """
    print("Запуск обновления глобальных предпочтений...")
    try:
        # 1. Получаем предпочтения ВСЕХ пользователей из БД
        #    Предполагаем, что db_api имеет такой метод.
        #    Он должен вернуть что-то вроде List[Dict[str, Dict[str, float]]]
        all_user_prefs = db_api.get_all_user_preferences()
        if not all_user_prefs:
            print("Не найдено предпочтений пользователей для обновления глобальных.")
            # Можно вернуть текущие глобальные или пустой словарь/дефолтные значения
            return db_api.get_global_preferences() # Возвращаем текущие, если ничего не нашли

        print(f"Получено предпочтений от {len(all_user_prefs)} пользователей.")

        # 2. Агрегируем оценки и счетчики для каждого атрибута/значения
        aggregated_scores = {attr: defaultdict(float) for attr in attributes}
        aggregated_counts = {attr: defaultdict(int) for attr in attributes}
        all_attribute_values = {attr: set() for attr in attributes} # Собираем все возможные значения

        for user_pref in all_user_prefs:
            for attr in attributes:
                # Проверяем, есть ли у пользователя предпочтения по этому атрибуту
                if attr in user_pref:
                    for value, score in user_pref[attr].items():
                        if score is not None: # Убедимся, что оценка существует
                           aggregated_scores[attr][value] += float(score) # Суммируем оценки
                           aggregated_counts[attr][value] += 1          # Считаем, сколько раз значение встречалось
                           all_attribute_values[attr].add(value)       # Добавляем значение в общий список

        # 3. Вычисляем средние значения для новых глобальных предпочтений
        new_global_preferences = {attr: {} for attr in attributes}
        for attr in attributes:
            # Используем все значения, встретившиеся хотя бы у одного пользователя
            for value in all_attribute_values[attr]:
                total_score = aggregated_scores[attr][value]
                count = aggregated_counts[attr][value]

                if count > 0:
                    average_score = total_score / count
                    new_global_preferences[attr][value] = average_score
                else:
                    # Этого не должно случиться при такой логике, но на всякий случай
                    # Можно установить дефолтное значение (например, 0 или взять из старых глобальных)
                    new_global_preferences[attr][value] = 0.0 # Или другое дефолтное значение

        # 5. Сохраняем обновленные глобальные предпочтения в БД
        #    Предполагаем, что db_api имеет такой метод.
        db_api.update_global_preferences(new_global_preferences)
        print("Глобальные предпочтения успешно обновлены.")

        return new_global_preferences

    except Exception as e:
        print(f"Ошибка при обновлении глобальных предпочтений: {e}")
        # В случае ошибки можно вернуть старые глобальные предпочтения
        try:
            return db_api.get_global_preferences()
        except Exception as db_e:
            print(f"Не удалось получить даже старые глобальные предпочтения: {db_e}")
            return {} 
        

def update_preferences_from_history(user_history, old_user_preferences, global_preferences, 
                                    attributes=['Main Genre', 'Sub Genre', 'Type', 'Author'], 
                                    prior_strength=10, alpha=0.1):
    user_pref_sum, user_count = collect_user_statistics(user_history, attributes)
    new_preferences = bayesian_update(global_preferences, user_pref_sum, user_count, prior_strength)

    updated_preferences = {attr: {} for attr in attributes}
    for attr in attributes:
        for val in global_preferences[attr]:
            old_value = old_user_preferences.get(attr, {}).get(val, global_preferences[attr].get(val, 0.5))
            new_value = new_preferences[attr].get(val, old_value)
            updated_preferences[attr][val] = (1 - alpha) * old_value + alpha * new_value
            
    return updated_preferences

def get_books_by_title(user_book_titles, clean_data):
    indices = []
    for title in user_book_titles:
        match = clean_data[clean_data['Title'].str.lower() == title.lower()]
        if not match.empty:
            indices.append(match.index[0])
        else:
            matches = process.extract(title, clean_data['Title'], limit=1)
            if matches and matches[0][1] > 60:
                closest_match = matches[0][0]
                fuzzy_match = clean_data[clean_data['Title'] == closest_match]
                if not fuzzy_match.empty:
                    indices.append(fuzzy_match.index[0])
                else:
                    print(f"Не найдено совпадение для книги (fuzzy): {title}")
            else:
                print(f"Не найдено совпадение для книги: {title}")
    return indices

def compute_explicit_weight(book, user_preferences):
    weight = 1.0
    for attr in ['Main Genre', 'Sub Genre', 'Type', 'Author']:
        attr_value = book[attr]
        if attr in user_preferences and attr_value in user_preferences[attr]:
            weight *= user_preferences[attr][attr_value]
    return weight

def zca_whitening(X, epsilon=1e-5):
    X_centered = X - np.mean(X, axis=0)
    sigma = np.cov(X_centered, rowvar=False)
    U, S, _ = np.linalg.svd(sigma)
    W = np.dot(U, np.dot(np.diag(1.0 / np.sqrt(S + epsilon)), U.T))
    X_whitened = np.dot(X_centered, W.T)
    return X_whitened



def compute_recommendations(user_id: int, user_book_titles: List[str], db_api: ServiceAPI) -> Dict[str, Any]:
    user_preferences = db_api.get_user_preferences(user_id)

    global_preferences = db_api.get_global_preferences()
    indices = get_books_by_title(user_book_titles, clean_data)
    user_books = [clean_data.iloc[ind] for ind in indices]
    user_preferences = update_preferences_from_history(user_books, user_preferences, global_preferences)
    db_api.update_user_preferences(user_id, user_preferences)
    book_preferences = [compute_explicit_weight(clean_data.iloc[idx], user_preferences) for idx in indices]
    books_vectors = features_whited[indices]
    user_profile = np.average(books_vectors, axis=0, weights=book_preferences)
    cosine_sim_scores = cosine_similarity(user_profile.reshape(1, -1), features_whited).flatten()
    top_indices = np.argsort(cosine_sim_scores)[::-1]
    filtered_indices = [idx for idx in top_indices if idx not in indices]
    rec_indices = filtered_indices[:10]
    recommended_titles = clean_data['Title'].iloc[rec_indices].tolist()
    return {"recommended_titles": recommended_titles}
db_api = ServiceAPI(base_url="http://localhost:8000")
books = pd.read_csv('./Books_df.csv')  # change to your path
clean_data = books.reset_index(drop=True)
encoder = OneHotEncoder(sparse_output=False)
features = encoder.fit_transform(clean_data[['Main Genre', 'Sub Genre', 'Type', 'Author']])
features_whited = zca_whitening(features)
ATTRIBUTES_FOR_PREFERENCES = ['Main Genre', 'Sub Genre', 'Type', 'Author']
initial_global_preferences = update_global_preferences(db_api, ATTRIBUTES_FOR_PREFERENCES)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)    




