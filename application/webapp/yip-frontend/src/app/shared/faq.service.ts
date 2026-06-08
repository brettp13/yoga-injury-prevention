import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { HttpService } from '../shared/http.service';

import { environment } from '../../environments/environment';
import { BehaviorSubject } from 'rxjs';

@Injectable()
export class FaqService {
    private api_url = environment.API_URL;
    faqs: BehaviorSubject<any>;
    httpHeaders = {};

    constructor(private http: HttpClient, private httpService: HttpService) {
        this.faqs = new BehaviorSubject([]);
    };

    getFaqs() {
        this.httpHeaders = this.httpService.createHeadersNoToken();
        this.http.get(this.api_url + '/faqs/list-faqs/', this.httpHeaders)
          .subscribe(
              (faqList) => {
                  console.log(faqList);
                  this.faqs.next(faqList);
              },
              (error) => {
                  console.log(error);
              }
          )
    };
}