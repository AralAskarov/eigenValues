import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';
import { RouterLink, RouterLinkActive, RouterOutlet } from '@angular/router';
import { Author, Book } from '../models';
import { BooksService } from '../books.service';

@Component({
  selector: 'app-library',
  standalone: true,
  imports: [CommonModule, RouterOutlet, RouterLink, RouterLinkActive,],
  templateUrl: './library.component.html',
  styleUrl: './library.component.css'
})
export class LibraryComponent {
   initialAuthor: Author = {
    id: 0,
    name: '',
    surname: '',
    birth_date: ''  
}
  books!: Book[];
  logged: boolean = false;
  newBook: Book = { id: null, title: '',  publishDate: '', description: '', thumbnail: '', averageRating: null, genre: '', author: this.initialAuthor  };
  constructor(private booksService: BooksService) { 
  }

  ngOnInit(): void {
    this.getBooks();
    const access: string|null = localStorage.getItem("access");
    if(access){
      this.logged = true;
    }
  }


  getBooks() : void {
    this.booksService.getBooks().subscribe((data) => {
      this.books = data;
    });
  }
  
}
