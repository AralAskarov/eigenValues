import { Component, NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { BooksService } from '../books.service';
import { Author, Book, Review, User2 } from '../models';

@Component({
  selector: 'app-reviews',
  moduleId: module.id,
  templateUrl: './reviews.component.html',
  styleUrls: ['./reviews.component.css']
})
export class ReviewsComponent {
  
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
    this.booksService.getReviews().subscribe((data) => {
      this.Reviews = data;
    });
  }
}

