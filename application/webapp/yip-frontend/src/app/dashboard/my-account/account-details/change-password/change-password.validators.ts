import { AbstractControl, AsyncValidatorFn, ValidationErrors } from '@angular/forms';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';

import { PasswordValidationService } from '../../../../shared/password-validation.service';

export class CurrentPasswordIncorrectValidator {
    static createValidator(passwordValidationService: PasswordValidationService): AsyncValidatorFn {
        return (control: AbstractControl): Observable<ValidationErrors> => {
            return passwordValidationService.validatePassword({'password': control.value}).pipe(
                map((result: boolean) => result ? null : {passwordIsInvalid: true})
            );
        };
    }
}
