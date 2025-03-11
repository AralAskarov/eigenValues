import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';
import { ActivatedRoute, RouterLink, RouterLinkActive, RouterOutlet } from '@angular/router';
import { BooksService } from '../books.service';
import {Location} from '@angular/common';
import { Book } from '../models';

@Component({
  selector: 'app-book-detail',
  standalone: true,
  imports: [CommonModule, RouterOutlet, RouterLink, RouterLinkActive],
  templateUrl: './book-detail.component.html',
  styleUrl: './book-detail.component.css'
})
export class BookDetailComponent {
  logged: boolean = false;
  book!: Book;

  
  constructor(private booksService: BooksService, private location: Location, private route: ActivatedRoute){

  }
  ngOnInit(): void {
    const access: string|null = localStorage.getItem("access");
    if(access){
      this.logged = true;
    }
    this.getBook();

    
  }
  getBook(): void {
    this.route.paramMap.subscribe((params) => {
      const idParam = params.get('id');
      if (idParam !== null) {
        const id = idParam;
        this.booksService.getBookDetails(id).subscribe((book) => {
          this.book = book;
      
      });
      }
    });
  }


  goBack(): void {
    this.location.back();
  }

}
