/**
*HEADER
*        arg/web/angular/src/app/components/toolbar/toolbar.component.ts
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
// Lib
import {Component, OnInit, ViewChild} from '@angular/core';
import {FormControl, FormGroup} from '@angular/forms';
import {saveAs} from 'file-saver';

// Services
import {ApiRequesterService} from './../../services/api-requester.service';
import {EventService} from './../../services/event.service';
import {LocalStorageService} from './../../services/local-storage.service';
import { Subscription } from 'rxjs';

@Component({
  selector: 'app-toolbar',
  templateUrl: './toolbar.component.html',
  styleUrls: ['./toolbar.component.scss']
})
export class ToolbarComponent implements OnInit {

  private defaultFormValues = {
    runOpt: '-e'
  }

  @ViewChild('openFileInput') openFileInput: any;
  public form = new FormGroup({
    runOpt: new FormControl(this.defaultFormValues.runOpt)
  });
  valueChangesSubscription: Subscription;

  /**
   * @constructor
   */
  constructor(
    private eventService: EventService,
    private apiRequestion: ApiRequesterService,
    private localStorageService: LocalStorageService
  ) {
  }

  /**
   * On component init
   */
  ngOnInit(): void {
    // form value change listener
    this.valueChangesSubscription = this.form.get('runOpt').valueChanges.subscribe(val => {
        this.localStorageService.setString(LocalStorageService.ARG_RUN_OPT_KEY, val);
    });
  }

  logResultError(result) : void {
    console.log()
    // Publish also error message
    if (result.error && result.error.message)
        this.eventService.publish('logger', { level: 'ERROR', message: result.error.message });
    else
      this.eventService.publish('logger', { level: 'ERROR', message: (result.message) ? result.message : 'Internal error' });
  }
  
  logResultLogs(result) : void {
    let logs = [];
    if (result.logs)
      logs = result.logs;
    else if (result.error && result.error.logs){ 
      logs = result.error.logs;
    }

    for (var i=0; i<logs.length;i++){
      var d = new Date(Date.parse(logs[i]['date']))
      this.eventService.publish('logger', { date: d, level: logs[i]['level'], message: logs[i]['message'] });
    }
  }

  /**
   * A function to be called each time that an api call fires an http error
   * @param result The result of the api call
   */
  onApiErrorResult(result): void {
    this.logResultLogs(result);
    this.logResultError(result);
  }

  /**
   * A function to call each time that an api call is successful (Http code = 200)
   * @param result The result of the api call
   */
  onApiSuccessResult(result): void {
    this.logResultLogs(result);
  }

  /**
   * Refresh tabs
   *
   * @return {void}
   */
  refreshTabs(): void {
    this.eventService.publish('report-information-tab-refresh', this.localStorageService.getJson(LocalStorageService.ARG_PARAMETERS_KEY));
    this.eventService.publish('general-options-tab-refresh', this.localStorageService.getJson(LocalStorageService.ARG_PARAMETERS_KEY));
    this.eventService.publish('data-options-tab-refresh', this.localStorageService.getJson(LocalStorageService.ARG_PARAMETERS_KEY));
    this.eventService.publish('inserts-tab-refresh', this.localStorageService.getJson(LocalStorageService.ARG_PARAMETERS_KEY));
  }


  /**
   * OpenFile Load the configuration file
   *
   * @return {void}
   */
  openFile(): void {
    // Check element exists
    if (this.openFileInput.nativeElement && this.openFileInput.nativeElement.files && 0 < this.openFileInput.nativeElement.files.length) {
      // Get file data
      let file: File = this.openFileInput.nativeElement.files.item(0);

      // Publish on logger
      this.eventService.publish('logger', {level: 'INFO', message: 'Requesting file load...'});

      // Post parameter file to arg
      this.apiRequestion.postParameters(file).subscribe(
        (result: any) => {
          
          // common processing of api response
          this.onApiSuccessResult(result);

          // update parameters locally
          this.localStorageService.setJson(LocalStorageService.ARG_PARAMETERS_KEY, result.parameters);

          // Trigger refresh on every tabs
          this.refreshTabs();
        },
        (error: any) => this.onApiErrorResult(error)
      );
    }
  }

  /**
   * Refresh
   *
   * @return {void}
   */
  reload(): void {

    // Publish on logger
    this.eventService.publish('logger', {level: 'INFO', message: 'Requesting reload...'});

    this.apiRequestion.postReload().subscribe(
      (result: any) => {

        // common processing of api response
        this.onApiSuccessResult(result);


        if (result.parameters && result.parameters !== null){
          // update parameters locally
          this.localStorageService.setJson(LocalStorageService.ARG_PARAMETERS_KEY, result.parameters);

          // Trigger refresh on every tabs
          this.refreshTabs();
        }
      },
      (error: any) => this.onApiErrorResult(error)
    );
  }

  /**
   * Save
   *
   * @return {void}
   */
  save(): void {
    let params = this.localStorageService.getJson(LocalStorageService.ARG_PARAMETERS_KEY);
    // check if any params exists
    if (params) {
      
      // Publish on logger
      this.eventService.publish('logger', {level: 'INFO', message: 'Requesting save...'});

      // Post parameter file to arg
      this.apiRequestion.postParametersToSave(params).subscribe(
        (result: File) => {

          // common processing of api response
          this.onApiSuccessResult(result);

          // Returns file
          saveAs(new File([result], 'parameters.yml'))

          // Publish on logger
          this.eventService.publish('logger', {
            level: 'SUCCESS',
            message: 'Parameters saved successfully'
          });

          // Trigger refresh on every tabs
          this.refreshTabs();
        },
        (error: any) => this.onApiErrorResult(error)
      );
    } else {
      // Publish on logger
      this.eventService.publish('logger', {level: 'INFO', message: 'Params needs to be provided'});
    }
  }

  /**
   * Paint
   *
   * @return {void}
   */
  paint(): void {
    alert("Paint");
  }

  /**
   * Runs arg
   *
   * @return {void}
   */
  run(): void {

    // Publish on logger
    this.eventService.publish('logger', { level: 'INFO', message: 'Requesting run action...' });

    var currentParameters = this.localStorageService.getJson(LocalStorageService.ARG_PARAMETERS_KEY);
    var activeParameters = Object.assign({ }, currentParameters);

    // Post active parameters to arg
    this.apiRequestion.postRun({ 
      parameters: activeParameters, 
      run_opt: this.localStorageService.getString(LocalStorageService.ARG_RUN_OPT_KEY)
    }).subscribe(
      (result: any) => this.onApiSuccessResult(result),
      (error: any) => this.onApiErrorResult(error)
    );
  }

  ngOnDestroy() {
    this.valueChangesSubscription.unsubscribe()
  }
}
