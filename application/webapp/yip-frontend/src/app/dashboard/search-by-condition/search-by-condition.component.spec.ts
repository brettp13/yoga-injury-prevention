import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { SearchByConditionComponent } from './search-by-condition.component';

describe('SearchByConditionComponent', () => {
  let component: SearchByConditionComponent;
  let fixture: ComponentFixture<SearchByConditionComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ SearchByConditionComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(SearchByConditionComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
