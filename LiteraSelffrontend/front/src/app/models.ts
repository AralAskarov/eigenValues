export interface Token {
    access: string;
    refresh: string;
}

export interface Review {
    id: number;
    rating: number;
    comment: string;
    created_at: string;
    book: Book | null; 
    user: string;

}
// export interface User {
//     username: string;
// }
export interface User {
    username: string;
    password: string;
    password2: string;
}

export interface Book {
    id: number | null;
    title: string;
    publishDate: string;
    description: string;
    thumbnail: string;
    averageRating: number | null;
    genre: string;
    author: Author | null;
    
}
export interface Author {
    id: number;
    name: string;
    surname: string;
    birth_date: string; 
}

export interface User2 {
    username: string;

}



