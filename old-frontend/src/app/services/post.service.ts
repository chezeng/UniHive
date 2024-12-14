import { HttpClient } from '@angular/common/http';
import { environment } from '../../environments/environment';

export class PostService {
  private apiUrl = environment.apiUrl;

  constructor(private http: HttpClient) {}

  getPosts() {
    return this.http.get(`${this.apiUrl}/posts/`);
  }
}
