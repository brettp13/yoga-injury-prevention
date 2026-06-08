import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs';
import { HttpClient } from '@angular/common/http';
import { HttpService } from './http.service';
import { environment } from '../../environments/environment';

@Injectable()
export class ForgotPasswordService {
    forgotPasswordForm: BehaviorSubject<boolean>;
    newPasswordSentAlert: BehaviorSubject<boolean>;
    httpHeaders = {};
    private api_url = environment.API_URL;

    constructor(private http: HttpClient,
                private httpService: HttpService) {
        this.forgotPasswordForm = new BehaviorSubject(false);
        this.newPasswordSentAlert = new BehaviorSubject(false);
    }

    showForgotPasswordForm() {
        this.forgotPasswordForm.next(true);
    }

    hideForgotPasswordForm() {
        this.forgotPasswordForm.next(false);
    }

    showPasswordSentAlert() {
        this.newPasswordSentAlert.next(true);
    }

    resetPassword(email: any) {
        var payload = {'email': email};
        this.httpHeaders = this.httpService.createHeadersNoToken();
        console.log('sending request');
        this.http.post(this.api_url + '/auth/forgot-password/', payload, this.httpHeaders)
          .subscribe(
              (response) => {
                  console.log(response);
              },
              (error) => {
                  console.log(error);
              }
          )
    }
}