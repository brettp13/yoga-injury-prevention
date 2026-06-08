import { Component, OnInit } from '@angular/core';
import { FormGroup, FormControl, Validators } from '@angular/forms';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';

import { environment } from '../../../../../environments/environment';
import { HttpService } from '../../../../shared/http.service';
import { NotificationService } from '../../../../shared/notifications.service';
import { UserService } from '../../../../shared/user.service';

@Component({
  selector: 'app-cancel-account',
  templateUrl: './cancel-account.component.html',
  styleUrls: ['./cancel-account.component.css']
})
export class CancelAccountComponent implements OnInit {
  cancelAccountForm: FormGroup;
  httpHeaders = {};
  token: string;
  private api_url = environment.API_URL;

  constructor(private http: HttpClient,
              private httpService: HttpService,
              private notificationService: NotificationService,
              private userService: UserService,
              private router: Router) { }

  ngOnInit() {
    this.cancelAccountForm = new FormGroup({
      'cancelReason': new FormControl(null, [Validators.required]),
    });

    this.userService.token.subscribe(
      (token) => {
        this.token = token;
      });
  }

  // shortcut function for cancel account form
  get cancelReason() { return this.cancelAccountForm.get('cancelReason') };

  cancelAccount() {
    this.httpHeaders = this.httpService.createHeadersWithToken(this.token);
    var payload = {'cancelReason': this.cancelReason.value};
    // dismiss modal
    (document.querySelector('.modal-backdrop.show') as HTMLElement).style.opacity = '0';

    this.http.post(this.api_url + '/auth/cancel-account/', payload, this.httpHeaders)
      .subscribe(
        (response) => {
          console.log(response);
          this.userService.signedOut();
          this.router.navigate(['']);
          this.notificationService.setAlert('cancel', 'Your account has been cancelled');
        },
        (error) => {
          console.log(error);
          this.userService.signedOut();
          this.router.navigate(['']);
        }
      )
  }
}
