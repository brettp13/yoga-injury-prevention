import { NgModule } from '@angular/core';

import { RouterModule, Routes } from '@angular/router';

import { LandingComponent } from './landing/landing.component';
import { PageNotFoundComponent } from './page-not-found/page-not-found.component';
import { HowItWorksComponent } from './how-it-works/how-it-works.component';
import { MeetTheTeamComponent } from './meet-the-team/meet-the-team.component';
import { BlogComponent } from './blog/blog.component';
import { BlogListComponent } from './blog/blog-list/blog-list.component';
import { BlogViewComponent } from './blog/blog-view/blog-view.component';
import { ContactUsPageComponent } from './contact-us-page/contact-us-page.component';
import { FaqPageComponent } from './faq-page/faq-page.component';
import { JoinPageComponent } from './join-page/join-page.component';
import { DashboardComponent } from './dashboard/dashboard.component';
import { DashboardHomeComponent } from './dashboard/dashboard-home/dashboard-home.component';
import { SearchByPoseComponent } from './dashboard/search-by-pose/search-by-pose.component';
import { SearchByConditionComponent } from './dashboard/search-by-condition/search-by-condition.component';
import { MyAccountComponent } from './dashboard/my-account/my-account.component';
import { AuthGuard } from './shared/guards/auth-guard.service';
import { AccountDetailsComponent } from './dashboard/my-account/account-details/account-details.component';
import { SubscriptionComponent } from './dashboard/my-account/subscription/subscription.component';
import { ViewPoseComponent } from './dashboard/view-pose/view-pose.component';
import { SearchbarComponent } from './dashboard/search-by-pose/searchbar/searchbar.component';
import { SearchComponent } from './dashboard/search-by-condition/search/search.component';
import { SearchResultsComponent } from './dashboard/search-by-condition/search-results/search-results.component';
import { ViewConditionComponent } from './dashboard/view-condition/view-condition.component';
import { ViewVideoComponent } from './dashboard/view-video/view-video.component';
import { FilterPosesComponent } from './dashboard/search-by-condition/filter-poses/filter-poses.component';
import { MedicalGlossaryComponent } from './medical-glossary/medical-glossary.component'; 

const appRoutes: Routes = [
    { path: '', component: LandingComponent },
    { path: 'how-it-works', component: HowItWorksComponent },
    { path: 'not-found', component: PageNotFoundComponent },
    { path: 'meet-the-team', component: MeetTheTeamComponent },
    { path: 'blog', component: BlogComponent, children: [
      {
        path: '', component: BlogListComponent,
      },
      {
        path: 'blog-view/:id', component: BlogViewComponent,
      }
    ] },
    { path: 'contact', component: ContactUsPageComponent },
    { path: 'faq', component: FaqPageComponent},
    { path: 'join-yip', component: JoinPageComponent },
    { path: 'dashboard', component: DashboardComponent, canActivate: [AuthGuard], children: [
      {
        path: '', component: DashboardHomeComponent, canActivate: [AuthGuard]
      },
      {
        path: 'search-by-pose', component: SearchByPoseComponent, canActivate: [AuthGuard], children: [
          {
            path: '', component: SearchbarComponent, canActivate: [AuthGuard]
          }
        ]
      },
      {
        path: 'pose-view', component: ViewPoseComponent, canActivate: [AuthGuard]
      },
      {
        path: 'medical-glossary', component: MedicalGlossaryComponent, canActivate: [AuthGuard]
      },
      {
        path: 'view-video', component: ViewVideoComponent, canActivate: [AuthGuard]
      },
      {
        path: 'search-by-condition', component: SearchByConditionComponent, canActivate: [AuthGuard], children: [
          {
            path: '', component: SearchComponent, canActivate: [AuthGuard]
          },
          {
            path: 'search-results', component: SearchResultsComponent, canActivate: [AuthGuard]
          },
          {
            path: 'filter-poses', component: FilterPosesComponent, canActivate: [AuthGuard]
          }
        ]
      },
      {
        path: 'view-condition', component: ViewConditionComponent, canActivate: [AuthGuard]
      },
      {
        path: 'my-account', component: MyAccountComponent, canActivate: [AuthGuard], children: [
          {
            path: '', component: AccountDetailsComponent, canActivate: [AuthGuard]
          },
          {
            path: 'subscription', component: SubscriptionComponent, canActivate: [AuthGuard]
          }
      ]}
    ]},
    { path: '**', redirectTo: '/not-found' },
  ]

@NgModule({
  imports: [
    RouterModule.forRoot(appRoutes, {scrollPositionRestoration: 'enabled'})
  ],
  exports: [RouterModule]
})
export class AppRoutingModule {
  
}