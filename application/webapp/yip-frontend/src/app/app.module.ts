import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { FormsModule, ReactiveFormsModule }   from '@angular/forms';
import { HttpClientModule } from '@angular/common/http';

import { Ng2SmartTableModule } from 'ng2-smart-table';

import { AppComponent } from './app.component';
import { MenuComponent } from './menu/menu.component';
import { LandingComponent } from './landing/landing.component';
import { PageNotFoundComponent } from './page-not-found/page-not-found.component';
import { AppRoutingModule } from './app-routing.module';
import { HowItWorksComponent } from './how-it-works/how-it-works.component';
import { FooterComponent } from './footer/footer.component';
import { MeetTheTeamComponent } from './meet-the-team/meet-the-team.component';
import { JoinFormComponent } from './join-form/join-form.component';
import { BlogComponent } from './blog/blog.component';
import { BlogMenuComponent } from './blog/blog-menu/blog-menu.component';
import { BlogListComponent } from './blog/blog-list/blog-list.component';
import { ContactUsPageComponent } from './contact-us-page/contact-us-page.component';
import { ContactComponent } from './contact-us-page/contact/contact.component';
import { FaqPageComponent } from './faq-page/faq-page.component';
import { FaqListComponent } from './faq-page/faq-list/faq-list.component';
import { SigninFormComponent } from './menu/signin-form/signin-form.component';
import { ContactService } from './contact-us-page/contact/contact.component.service';
import { SignupService } from './shared/signup.service';
import { DashboardComponent } from './dashboard/dashboard.component';
import { SearchByPoseComponent } from './dashboard/search-by-pose/search-by-pose.component';
import { DashboardHomeComponent } from './dashboard/dashboard-home/dashboard-home.component';
import { SearchByConditionComponent } from './dashboard/search-by-condition/search-by-condition.component';
import { EmailValidationService } from './shared/email-validation.service';
import { UserService } from './shared/user.service';
import { SearchComponent } from './dashboard/search-by-condition/search/search.component';
import { ConditionsService } from './shared/conditions.service';
import { UserProfileService } from './shared/user.profile.service';
import { AuthGuard } from './shared/guards/auth-guard.service';
import { UtilsService } from './dashboard/search-by-condition/search/utils.service';
import { YogaPoseService } from './shared/yogapose.service';
import { JoinPageComponent } from './join-page/join-page.component';
import { BlogService } from './blog/blog.service';
import { FaqService } from './shared/faq.service';
import { BlogViewComponent } from './blog/blog-view/blog-view.component';
import { SafeHtmlPipe } from './shared/format-html.pipe';
import { MyAccountComponent } from './dashboard/my-account/my-account.component';
import { AccountDetailsComponent } from './dashboard/my-account/account-details/account-details.component';
import { ChangePasswordComponent } from './dashboard/my-account/account-details/change-password/change-password.component';
import { PasswordValidationService } from './shared/password-validation.service';
import { SubscriptionComponent } from './dashboard/my-account/subscription/subscription.component';
import { HttpService } from './shared/http.service';
import { ViewPoseComponent } from './dashboard/view-pose/view-pose.component';
import { SearchbarComponent } from './dashboard/search-by-pose/searchbar/searchbar.component';
import { FilterPipe } from './dashboard/search-by-pose/searchbar/filter.pipe';
import { ConditionFilterPipe } from './dashboard/search-by-condition/search/filter.pipe';
import { SearchResultsComponent } from './dashboard/search-by-condition/search-results/search-results.component';
import { ViewConditionComponent } from './dashboard/view-condition/view-condition.component';
import { ForgotPasswordComponent } from './menu/signin-form/forgot-password/forgot-password.component';
import { ForgotPasswordService } from './shared/forgot-password.service';
import { CancelAccountComponent } from './dashboard/my-account/account-details/cancel-account/cancel-account.component';
import { NotificationService } from './shared/notifications.service';
import { SearchConditionService } from './shared/search-conditions.service';
import { FilterPosesComponent } from './dashboard/search-by-condition/filter-poses/filter-poses.component';
import { FilterPoseService } from './shared/filter-poses.service';
import { VideoService } from './shared/video.service';
import { ViewVideoComponent } from './dashboard/view-video/view-video.component';
import { MedicalGlossaryComponent } from './medical-glossary/medical-glossary.component';



@NgModule({
  declarations: [
    AppComponent,
    MenuComponent,
    LandingComponent,
    PageNotFoundComponent,
    HowItWorksComponent,
    FooterComponent,
    MeetTheTeamComponent,
    JoinFormComponent,
    BlogComponent,
    BlogMenuComponent,
    BlogListComponent,
    ContactUsPageComponent,
    ContactComponent,
    FaqPageComponent,
    FaqListComponent,
    SigninFormComponent,
    DashboardComponent,
    SearchByPoseComponent,
    DashboardHomeComponent,
    SearchByConditionComponent,
    SearchComponent,
    JoinPageComponent,
    BlogViewComponent,
    SafeHtmlPipe,
    MyAccountComponent,
    AccountDetailsComponent,
    ChangePasswordComponent,
    SubscriptionComponent,
    ViewPoseComponent,
    SearchbarComponent,
    FilterPipe,
    ConditionFilterPipe,
    SearchResultsComponent,
    ViewConditionComponent,
    ForgotPasswordComponent,
    CancelAccountComponent,
    FilterPosesComponent,
    ViewVideoComponent,
    MedicalGlossaryComponent,
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    FormsModule,
    ReactiveFormsModule,
    HttpClientModule,
    Ng2SmartTableModule,
  ],
  providers: [
    ContactService,
    SignupService,
    EmailValidationService,
    UserService,
    ConditionsService,
    UserProfileService,
    AuthGuard,
    UtilsService,
    YogaPoseService,
    BlogService,
    FaqService,
    PasswordValidationService,
    HttpService,
    ForgotPasswordService,
    NotificationService,
    SearchConditionService,
    FilterPoseService,
    VideoService,
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
