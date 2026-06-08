import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs';

@Injectable()
export class NotificationService {
    alert: BehaviorSubject<boolean>;
    alertType: BehaviorSubject<string>;
    alertText: BehaviorSubject<string>;

    constructor() {
        this.alert = new BehaviorSubject(false);
        this.alertType = new BehaviorSubject('');
        this.alertText = new BehaviorSubject('');
    }

    setAlert(alertType:string, alertText: string) {
        this.alert.next(true);
        this.alertType.next(alertType);
        this.alertText.next(alertText);
    }
}