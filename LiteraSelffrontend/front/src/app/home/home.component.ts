import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';
import { RouterLink, RouterLinkActive, RouterOutlet } from '@angular/router';
import { BooksService } from '../books.service';

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [CommonModule, RouterOutlet, RouterLink, RouterLinkActive],
  templateUrl: './home.component.html',
  styleUrl: './home.component.css'
})
export class HomeComponent {
  title:string = 'Connection to Django app';
  logged: boolean = false;


  
  constructor(private booksService: BooksService){

  }

  ngOnInit() : void {
    const access: string|null = localStorage.getItem("access");
    if(access){
      this.logged = true;
    }
  }
}
