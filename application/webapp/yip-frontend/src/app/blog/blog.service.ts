import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Router } from '@angular/router';

import { BehaviorSubject } from 'rxjs';

import { environment } from '../../environments/environment';

@Injectable()
export class BlogService {
    private api_url = environment.API_URL;
    blogPosts: BehaviorSubject<any>;
    blogPost: BehaviorSubject<any>;
    author: BehaviorSubject<any>;
    selectedBlogPost: BehaviorSubject<any>;
    postIsSelected: BehaviorSubject<boolean>;

    httpOptions = {
        headers: new HttpHeaders({ 'Content-Type': 'application/json' })
    };

    
    constructor(private http: HttpClient,
                private router: Router) {
        this.blogPosts = new BehaviorSubject([]);
        this.blogPost = new BehaviorSubject([]);
        this.author = new BehaviorSubject([]);
        this.selectedBlogPost = new BehaviorSubject([]);
        this.postIsSelected = new BehaviorSubject(false);
    };

    listOfBlogPosts(blogPosts: Array<[]>) {
        console.log('List of blog posts:');
        console.log(blogPosts);
        this.blogPosts.next(blogPosts);
    }

    getBlogPosts() {
        this.http.get(this.api_url + '/blog/list-blog-posts/', this.httpOptions)
          .subscribe(
              (response: any) => {
                  this.listOfBlogPosts(response);
                  this.selectedBlogPost.next(response[0]);
              },
              (error) => {
                  console.log(error);
              }
          )
    }

    getBlogPost(id: number) {
        this.http.post(this.api_url + '/blog/select-blog-post/', {'blog_post_id': id}, this.httpOptions)
          .subscribe(
              (blogPost: any) => {
                  this.blogPost.next(blogPost);
                  this.getBlogPostAuthor(blogPost.author);
              },
              (error) => {
                  console.log(error);
              }
          )
    }

    getBlogPostAuthor(id: number) {
        this.http.post(this.api_url + '/blog/select-author/', {'author_id': id}, this.httpOptions)
          .subscribe(
              (author) => {
                  this.author.next(author);
              },
              (error) => {
                  console.log(error);
              }
          )
    }

    selectBlogPost(blogPost) {
        this.postIsSelected.next(true);
        this.selectedBlogPost.next(blogPost);
        this.router.navigate(['/blog/blog-view', blogPost.id]);
    }

    selectBlogList() {
        this.postIsSelected.next(false);
        this.router.navigate(['/blog']);
    }
}