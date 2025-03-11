import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';
import { RouterLink, RouterLinkActive, RouterOutlet } from '@angular/router';
import { BooksService } from '../books.service';
import { Author, Book, Review, User, User2 } from '../models';
import { FormsModule } from '@angular/forms';
@Component({
  selector: 'app-search',
  standalone: true,
  imports: [CommonModule, RouterOutlet, RouterLink, RouterLinkActive,FormsModule, CommonModule ],
  templateUrl: './search.component.html',
  styleUrl: './search.component.css'
})
export class SearchComponent {
  Reviews!: Review[];
  logged: boolean = false;


  constructor(private booksService: BooksService) { 
  }

  ngOnInit(): void {
    this.getReviews();
    const access: string|null = localStorage.getItem("access");
    if(access){
      this.logged = true;
    }
  }
  getReviews(): void {
    this.booksService.getReviews().subscribe({
      next: (data) => {
        this.Reviews = data;
      },
      error: (err) => {
        console.error('Failed to fetch reviews:', err);
      }
    });
  }
}
