import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';

import { UserService } from '../../../shared/user.service';
import { YogaPoseService } from '../../../shared/yogapose.service';


@Component({
  selector: 'app-searchbar',
  templateUrl: './searchbar.component.html',
  styleUrls: ['./searchbar.component.css', './slider.css']
})
export class SearchbarComponent implements OnInit {
  token: string;
  searchText = '';
  poses: any;
  listView: boolean = false
  isListView: any;
  searchResults: number = 0;
  
  constructor(private yogaPoseService: YogaPoseService,
              private router: Router,
              private userService: UserService) { }

  ngOnInit() {
    this.userService.token.subscribe(
      (newToken) => {
        this.token = newToken;
      });

    this.yogaPoseService.listOfPoses.subscribe(
      (newListOfPoses) => {
        this.poses = newListOfPoses;
        // debug statement
        console.log(this.poses);
      });

    this.yogaPoseService.listView.subscribe(
      isListView => {
      this.isListView = isListView;
    });

    this.yogaPoseService.getPoses(this.token);

    this.yogaPoseService.setSearchResults(0);
    
    this.yogaPoseService.searchResults.subscribe(
      (results) => {
        this.searchResults = +results;
      });
  }

  setListView() {
    this.yogaPoseService.setListView();
  }

  viewPose(id: number) {
    this.yogaPoseService.selectPose(this.token, id);
    this.yogaPoseService.getConditionsContraindicatedByPose(id, this.token);
    this.yogaPoseService.getConditionsHelpedByPose(id, this.token);
    this.router.navigate(['dashboard', 'pose-view']);
  }
}
