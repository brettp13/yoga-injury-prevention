import { Component, OnInit } from '@angular/core';

import { FaqService } from '../../shared/faq.service';

@Component({
  selector: 'app-faq-list',
  templateUrl: './faq-list.component.html',
  styleUrls: ['./faq-list.component.css']
})
export class FaqListComponent implements OnInit {
  faqs: any;

  constructor(private faqService: FaqService) { }

  ngOnInit() {
    this.faqService.faqs.subscribe(
      (faqList) => {
        this.faqs = faqList;
      });
    this.faqService.getFaqs();
  }

}
