import { Component, OnInit } from '@angular/core';

import { BlogService } from './blog.service';

@Component({
  selector: 'app-blog',
  templateUrl: './blog.component.html',
  styleUrls: ['./blog.component.css']
})
export class BlogComponent implements OnInit {
  blogPost: any;
  postIsSelected: boolean;

  constructor(private blogService: BlogService) { }

  ngOnInit() {
    this.blogService.selectedBlogPost.subscribe(
      (blogPost) => {
        this.blogPost = blogPost;
      });

    this.blogService.getBlogPosts();

    this.blogService.postIsSelected.subscribe(
      (boolean) => {
        this.postIsSelected = boolean;
      });
  }

  selectPost(blogPost) {
    this.blogService.selectBlogPost(blogPost);
  }
}
