import { Component, OnInit } from '@angular/core';

import { NotificationService } from '../shared/notifications.service';

@Component({
  selector: 'app-landing',
  templateUrl: './landing.component.html',
  styleUrls: [
    './css/general-styles.css', 
    './css/video-section.css',
    './css/info-section.css',
    './css/benefits-section.css',
    './css/experts-section.css',
    './css/landing.component.media.queries.css',]
})
export class LandingComponent implements OnInit {
  alert: boolean;
  alertType: string;
  alertText: string;

  constructor(private notificationService: NotificationService) { }

  ngOnInit() {
    this.notificationService.alert.subscribe(
      (alert) => {
        this.alert = alert;
      });

    this.notificationService.alertType.subscribe(
      (alertType) => {
        this.alertType = alertType;
      });

    this.notificationService.alertText.subscribe(
      (alertText) => {
        this.alertText = alertText;
      });
  }
}
