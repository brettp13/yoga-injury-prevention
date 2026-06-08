import { Component, OnInit } from '@angular/core';

import { BlogService } from '../blog.service';

@Component({
  selector: 'app-blog-list',
  templateUrl: './blog-list.component.html',
  styleUrls: ['./blog-list.component.css']
})
export class BlogListComponent implements OnInit {
  blogPosts: any;

  constructor(private blogService: BlogService) { }

  ngOnInit() {
    this.blogService.blogPosts.subscribe(
      (blogPosts) => {
        this.blogPosts = blogPosts
      });
    this.blogService.getBlogPosts();
  }

  selectBlogPost(blogPost) {
    this.blogService.selectBlogPost(blogPost);
  }
}
