import {AbstractControl, AsyncValidatorFn, ValidationErrors} from '@angular/forms';
import {Observable} from 'rxjs';
import {map} from 'rxjs/operators';

import { EmailValidationService } from '../shared/email-validation.service';

export class EmailIsTakenValidator {
  static createValidator(emailValidationService: EmailValidationService): AsyncValidatorFn {
    return (control: AbstractControl): Observable<ValidationErrors> => {
      return emailValidationService.validateEmail({'email': control.value}).pipe(
        map((result: boolean) => result ? null : {emailIsTaken: true})
      );
    };
  }
}