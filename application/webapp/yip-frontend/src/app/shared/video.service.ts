import { Injectable } from '@angular/core';

import { BehaviorSubject } from 'rxjs';

@Injectable()
export class VideoService {
    videoUrl: BehaviorSubject<string> = new BehaviorSubject('');
}