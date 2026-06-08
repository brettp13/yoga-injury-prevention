import { Component, OnInit } from '@angular/core';

import { BlogService } from '../blog.service';

@Component({
  selector: 'app-blog-menu',
  templateUrl: './blog-menu.component.html',
  styleUrls: ['./blog-menu.component.css']
})
export class BlogMenuComponent implements OnInit {

  constructor(private blogService: BlogService) { }

  ngOnInit() {
  }

  selectBlogList() {
    this.blogService.selectBlogList();
  }

}
