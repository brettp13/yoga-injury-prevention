import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';

import { BlogService } from '../blog.service';

@Component({
  selector: 'app-blog-view',
  templateUrl: './blog-view.component.html',
  styleUrls: ['./blog-view.component.css']
})
export class BlogViewComponent implements OnInit {
  blogId: number;
  blogPost: any;
  author: any;

  constructor(private activatedRoute: ActivatedRoute, private blogService: BlogService) { }

  ngOnInit(): void {
    this.blogService.blogPost.subscribe(
      (blogPost) => {
        this.blogPost = blogPost;
    });

    this.blogService.author.subscribe(
      (author) => {
        this.author = author;
    });

    this.blogId = +this.activatedRoute.snapshot.paramMap.get("id");
    this.blogService.getBlogPost(this.blogId);
  }

}
