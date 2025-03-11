import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { Router, RouterLink, RouterLinkActive, RouterOutlet } from '@angular/router';
import { BooksService } from '../books.service';
import { User } from '../models';

@Component({
  selector: 'app-registration',
  standalone: true,
  imports: [CommonModule, RouterOutlet, RouterLink, RouterLinkActive, FormsModule],
  templateUrl: './registration.component.html',
  styleUrl: './registration.component.css'
})
export class RegistrationComponent {
  newUser: User = { username: '', password: '', password2: ''};
  logged: boolean = false;


  constructor(private booksService: BooksService, private router: Router){}
  ngOnInit() : void {
    const access: string|null = localStorage.getItem("access");
    if(access){
      this.logged = true;
    }
  }
  
  registration(): void {
    if (this.newUser !== null) {
      this.booksService
        .register(this.newUser)
        .subscribe((data: User) => {
          this.newUser = { username: '', password: '', password2: ''};
        });
    } else {
      alert("Please, enter date")
    }
  }


}
