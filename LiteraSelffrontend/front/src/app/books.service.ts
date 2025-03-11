import { Injectable } from '@angular/core';
import { Observable, throwError  } from 'rxjs';
import {Book, Review, Token, User} from "./models"
import { HttpClient } from '@angular/common/http';
import { BehaviorSubject } from 'rxjs';
import { tap, catchError, map } from 'rxjs/operators';

@Injectable({
  providedIn: 'root'
})
export class BooksService {

  BASE_URL:string = `http://127.0.0.1:8000`;
  // API_URL:string = `https://www.googleapis.com/books/v1/volumes?q=`;
  // key: string = `&key=AIzaSyC1A0nWbTH2lngwHsagiDeKWjVHH2A2A4c`;
  constructor(private http: HttpClient) { }
  // http://localhost:4200/home?state=STATE_STRING%20%D1%87%D1%82%D0%BE%20%D0%B2%D0%B2%D0%B5%D1%81%D1%82%D0%B8%20%D0%BD%D0%B0%20%D0%BC%D0%B5%D1%81%D1%82%D0%B5%20YOUR_REDIRECT_URI&code=4%2F0AeaYSHCoe7Hx15TcKyKQ-NxpJPGEU9_754yw48RMwKeXMzuf04kF151KlEe_Ewnrod_6Zg&scope=email%20openid%20https:%2F%2Fwww.googleapis.com%2Fauth%2Fuserinfo.email&authuser=0&prompt=consent
  // https://oauth2.googleapis.com/token
  // code 4/0AeaYSHDqP3L2gBCZS9OHd7WN282j5DvD2Yf_6NcNtR2n5K5_SkeW6C0bMCncavVTtAmxjg
  // client_id  1054617542150-9iinulvff135o7ln52bfrqc3qnmrt2e7.apps.googleusercontent.com
  // client_secret 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
  // redirect_uri http://localhost:4200/home
  // grant_type authorization_code
  // {
  //   "access_token": "ya29.a0Ad52N38xNhFoRDocduPTtvp7wL65rTmA-VXf3Aeiy4a3tvAnpyFj86vcAEInP1McKXOd3r4U0MqPwBA2JBF1_VYZNaw9Z0a_KZkxp19fy70KuYz309DllDtLeRNAGMFJDennd9YceHztJpxmSDFesd1-9czDpeDZT9k_aCgYKAY8SARMSFQHGX2MiNX6AUVZXgTowEmmvkMXpqA0171",
  //   "expires_in": 3599,
  //   "scope": "https://www.googleapis.com/auth/userinfo.email openid",
  //   "token_type": "Bearer",
  //   "id_token": "eyJhbGciOiJSUzI1NiIsImtpZCI6ImUxYjkzYzY0MDE0NGI4NGJkMDViZjI5NmQ2NzI2MmI2YmM2MWE0ODciLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL2FjY291bnRzLmdvb2dsZS5jb20iLCJhenAiOiIxMDU0NjE3NTQyMTUwLTlpaW51bHZmZjEzNW83bG41MmJmcnFjM3FubXJ0MmU3LmFwcHMuZ29vZ2xldXNlcmNvbnRlbnQuY29tIiwiYXVkIjoiMTA1NDYxNzU0MjE1MC05aWludWx2ZmYxMzVvN2xuNTJiZnJxYzNxbm1ydDJlNy5hcHBzLmdvb2dsZXVzZXJjb250ZW50LmNvbSIsInN1YiI6IjExNTM3OTQ5NzI1NTAwODExMTk4MyIsImVtYWlsIjoiYXNrYXJvdi4xMC4wOUBnbWFpbC5jb20iLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwiYXRfaGFzaCI6ImU1d1ZmVXlLd21xY2dOaTZNX1kyb1EiLCJpYXQiOjE3MTM5NTQ3OTgsImV4cCI6MTcxMzk1ODM5OH0.cFjAc5xRvQ7ZCD8ehSCevZxJpvMheB20RcdhzTB5Da5mC9OTgBtg9k25WfYiw-jVRFG1O7iHOH7jY13j1XPpFd_6ldWXitwN5PFYTPIhicSroi8QFk_i-jvZMsbRg855mh82j6IDFyw_KifHZSZrYrDiEnMLpRtzbIPm2NwGjlKcJ4UuJDZzd6IkylnZhDC9ykMrmNHDEcMtNO8sFbRFyj6T_QKSuGJEVM_7iQ7lmOeMkUNPchX7ZkvOz0o-ymLuVMo7o8MedCokacsqaGh7DKBDj05kqi5CPdNkIqknDSUVrteUMLu5wWCVNR62zh_hptOZG1-jBwVGKYd5vmO7DQ"
  // }


  // https://www.googleapis.com/books/v1/volumes?q=subject:fantasy&maxResults=10&key=AIzaSyC1A0nWbTH2lngwHsagiDeKWjVHH2A2A4c
  // let responseData = JSON.parse(responseBody);
  // postman.setEnvironmentVariable("access_token", responseData.access);
  // Authorization Bearer {{access_token}}


  register(user: User): Observable<User>{
    return this.http.post<User>(`${this.BASE_URL}/api/registration/`, user );
  }



  login(username:string,password:string): Observable<Token> {
    return this.http.post<Token>(`${this.BASE_URL}/login/`, {username,password});
  }




  getBooks(): Observable<Book[]> {
    return this.http.get<Book[]>(`${this.BASE_URL}/api/book`).pipe(
      map(books => books.map(book => ({
        id: book.id,
        title: book.title,
        author: book.author,
        publishDate: book.publishDate,
        description: book.description,
        thumbnail: book.thumbnail,
        averageRating: book.averageRating || 0, // Предполагаем, что рейтинг может быть не указан
        genre: book.genre || 'Unknown' // Добавьте жанр, если он не указан
      })))
    );
  }

  getBookDetails(bookId: string): Observable<Book> {
    return this.http.get<Book>(`${this.BASE_URL}/api/book/${bookId}`);
  }

  postbook(book: Book): Observable<Book> {
    return this.http.post<Book>(`${this.BASE_URL}/api/book`, book);

  }
  
  getReviews(): Observable<Review[]> {
    // alert(1)
    return this.http.get<Review[]>(`${this.BASE_URL}/api/review`);
  }
}
