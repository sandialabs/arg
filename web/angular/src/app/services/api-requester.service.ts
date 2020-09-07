/**
*HEADER
*           arg/web/angular/src/app/services/api-requester.service.ts
*                Automatic Report Generator (ARG) v. 1.0
*
*  Copyright 2020 National Technology & Engineering Solutions of Sandia, LLC
*  (NTESS). Under the terms of Contract DE-NA0003525 with NTESS, the U.S.
*  Government retains certain rights in this software.
*
*  Redistribution and use in source and binary forms, with or without
*  modification, are permitted provided that the following conditions are met:
*
*  * Redistributions of source code must retain the above copyright notice,
*    this list of conditions and the following disclaimer.
*
*  * Redistributions in binary form must reproduce the above copyright notice,
*    this list of conditions and the following disclaimer in the documentation
*    and/or other materials provided with the distribution.
*
*  * Neither the name of the copyright holder nor the names of its
*    contributors may be used to endorse or promote products derived from this
*    software without specific prior written permission.
*
*  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
*  AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
*  IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
*  ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
*  LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
*  CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUENT OF
*  SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
*  INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
*  CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
*  ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
*  POSSIBILITY OF SUCH DAMAGE.
*
*  Questions? Visit gitlab.com/AutomaticReportGenerator/arg
*
*HEADER
*/
import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';

import { environment } from './../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class ApiRequesterService {
  /**
   * @constructor
   */
  constructor(
    private http: HttpClient
  ) { }

  /**
   * Get default parameters
   * @return [description]
   */
  getDefaultParameters(): Observable<any> {
    return this.http.get(`${environment.apiUrl}/api/v1/arg/parameters/default`);
  }

  /**
   * Post a run request
   * @param runParameters parameters for arg run
   */
  postRun(runParameters: object): Observable<any> {
    // In progress (Thomas)
    return this.http.post(`${environment.apiUrl}/api/v1/arg/run`, runParameters);
  }

  /**
   * Post a reload request
   */
  postReload(): Observable<any> {
    // Send request and return Observable
    return this.http.post(`${environment.apiUrl}/api/v1/arg/reload`, null);
  }

  /**
   * Post parameters file
   * @param  file [description]
   * @return      [description]
   */
  postParameters(file: File): Observable<any> {
    // Create FormData
    let formData: FormData = new FormData();

    // Add file to form data
    formData.append('file', file);

    // Prepare headers
    let headers = new HttpHeaders();
    headers.append('Content-Type', 'multipart/form-data');
    headers.append('Accept', 'application/json');

    // Create options
    let options: any = { headers: headers };

    // Send request and return Observable
    return this.http.post(`${environment.apiUrl}/api/v1/arg/parameters/read`, formData, options);
  }

    /**
   * Post parameters file
   * @param  params [description]
   * @return      [description]
   */
  postParametersToSave(params: object): Observable<any> {
    // Prepare headers
    let headers = new HttpHeaders();
    headers.append('Accept', 'multipart/form-data');
    headers.append('Content-Type', 'application/json');

    // Create options
    let options: any = { headers: headers, responseType: "blob"};

    // Send request and return Observable
    return this.http.post(`${environment.apiUrl}/api/v1/arg/parameters/write`, params, options);
  }

}
