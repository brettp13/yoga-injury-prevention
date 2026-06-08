import { Component, OnInit } from '@angular/core';
import { DomSanitizer } from '@angular/platform-browser';
import { Location } from '@angular/common';

import { VideoService } from '../../shared/video.service';

@Component({
  selector: 'app-view-video',
  templateUrl: './view-video.component.html',
  styleUrls: ['./view-video.component.css']
})
export class ViewVideoComponent implements OnInit {
  video: any;

  constructor(private domSanitizer: DomSanitizer, 
              private videoService: VideoService,
              private location: Location) { }

  ngOnInit() {
    this.videoService.videoUrl.subscribe(
      (videoUrl) => {
        this.video = this.domSanitizer.bypassSecurityTrustResourceUrl(videoUrl);      
      });
    console.log(this.video);
  }

  back() {
    this.location.back(); 
  }
}
