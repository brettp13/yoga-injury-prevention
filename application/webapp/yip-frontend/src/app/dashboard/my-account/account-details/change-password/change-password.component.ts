import { Component, OnInit } from '@angular/core';
import { FormGroup, FormControl, Validators } from '@angular/forms';

import { UserService } from '../../../../shared/user.service';
import { CurrentPasswordIncorrectValidator } from './change-password.validators';
import { PasswordValidationService } from 'src/app/shared/password-validation.service';

@Component({
  selector: 'app-change-password',
  templateUrl: './change-password.component.html',
  styleUrls: ['./change-password.component.css']
})
export class ChangePasswordComponent implements OnInit {
  changePasswordForm: FormGroup;
  token: string;

  constructor(private userService: UserService, 
              private passwordValidationService: PasswordValidationService) { }

  ngOnInit() {
     this.changePasswordForm = new FormGroup({
      'currentPassword': new FormControl(
        null, 
        [Validators.required], 
        CurrentPasswordIncorrectValidator.createValidator(this.passwordValidationService)
      ),
     });
     // Add the newPassword and verifyNewPassword controls separately so we can use our 
     // custom validator
     this.changePasswordForm.addControl('newPassword', new FormControl('', [Validators.required]));
     this.changePasswordForm.addControl('verifyNewPassword', new FormControl(
       '', [Validators.compose(
           [Validators.required, this.validateAreEqual.bind(this)]
       )]
     ));

    this.userService.token.subscribe(
      (token) => {
        this.token = token;
      });
  }

  private validateAreEqual(fieldControl: FormControl) {
    if (fieldControl.value === "") {
      return fieldControl.value === this.changePasswordForm.get("newPassword").value ? null : {
        passwordsMustMatch: false
      };
    } else {
      return fieldControl.value === this.changePasswordForm.get("newPassword").value ? null : {
        passwordsMustMatch: true
      };
    }
  }

  // shortcut functions
  get f() { return this.changePasswordForm.controls; }

  onSubmit() {
    this.userService.updateAuthInfo(this.token, [{'password': this.f.verifyNewPassword.value}]);

  }

}
