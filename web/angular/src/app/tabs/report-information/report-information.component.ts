/**
*HEADER
*../web/angular/src/app/tabs/report-information/report-information.component.ts
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
// Libs
import {Component, OnInit} from '@angular/core';
import {FormControl, FormGroup} from '@angular/forms';

// Services
import {ApiRequesterService} from './../../services/api-requester.service';
import {EventService} from './../../services/event.service';
import {LocalStorageService} from './../../services/local-storage.service';
import {Subscription} from 'rxjs';

@Component({
  selector: 'app-report-information',
  templateUrl: './report-information.component.html',
  styleUrls: ['./report-information.component.scss']
})
export class ReportInformationComponent implements OnInit {

  /**
   * @variables
   */
  private defaultFormValues = {
    BackendType: "LaTeX",
    ReportType: "Report",
    Mutables: "",
    StructureFile: "",
    StructureEnd: "",
    ArtifactFile: "",
    OutputDir: "",
    Verbosity: "1"

  };
  public form = new FormGroup({
    BackendType: new FormControl(this.defaultFormValues.BackendType),
    ReportType: new FormControl(this.defaultFormValues.ReportType),
    Mutables: new FormControl(this.defaultFormValues.Mutables),
    StructureFile: new FormControl(this.defaultFormValues.StructureFile),
    StructureEnd: new FormControl(this.defaultFormValues.StructureEnd),
    ArtifactFile: new FormControl(this.defaultFormValues.ArtifactFile),
    OutputDir: new FormControl(this.defaultFormValues.OutputDir),
    Verbosity: new FormControl(this.defaultFormValues.Verbosity)
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
   * On init
   * @return {void}
   */
  ngOnInit(): void {
    // Check is default conf
    let isDefaultConf: boolean = this.localStorageService.getBoolean(LocalStorageService.IS_DEFAULT_CONF);

    // Set default config if no config yet
    if (undefined == isDefaultConf) {

      console.log('Init default configuration')

      // Set to true
      this.localStorageService.setBoolean(LocalStorageService.IS_DEFAULT_CONF, true);

      var defaultParameters = {}
      Object.assign(defaultParameters, this.defaultFormValues);

     
      this.localStorageService.setJson(LocalStorageService.ARG_PARAMETERS_KEY, defaultParameters);
      this.localStorageService.setString(LocalStorageService.ARG_RUN_OPT_KEY, "-e");

      // Get default configuration from api
      this.apiRequestion.getDefaultParameters().subscribe(
        (result: any) => {


          console.log("Init default configuration using api default configuration")
          
          // Set configuration
          this.localStorageService.setJson(LocalStorageService.ARG_PARAMETERS_KEY, result);

          // Publish on logger
          this.eventService.publish('logger', {level: 'INFO', message: "Default parameters applied."});

          // Reload current tab (other tabs will be reloaded when going to)
          this.eventService.publish('report-information-tab-refresh', this.localStorageService.getJson(LocalStorageService.ARG_PARAMETERS_KEY));
        },
        (error: any) => {
          // Publish on logger
          this.eventService.publish('logger', {level: 'ERROR', message: error.message});

          this.localStorageService.setJson(LocalStorageService.ARG_PARAMETERS_KEY, {})
        }
      );
    }

    // Refresh listener
    this.eventService.subscribe('report-information-tab-refresh',
      (data: any) => {

        if ("object" == typeof data) {

          // Reset form
          this.form.reset();

          // Get defaults
          let formData: any = this.defaultFormValues;

          // Prepare new data
          Object.keys(data).forEach((key) => {
            if (this.form.contains(key)) {
              if (typeof data[key] == 'number') {
                data[key] = data[key].toString();
              }
              
              if (formData[key] !== data[key]){
                formData[key] = data[key];
              }
            }
          });

          // Set form data
          this.form.setValue(formData);
        }
      }
    );

    // Refresh the first time
    this.eventService.publish('report-information-tab-refresh', this.localStorageService.getJson(LocalStorageService.ARG_PARAMETERS_KEY));

    // form value change listener
    this.valueChangesSubscription = this.form.valueChanges.subscribe(val => {
      // Get current storage configuration
      let currentPConfig = this.localStorageService.getJson(LocalStorageService.ARG_PARAMETERS_KEY);
      let state = JSON.stringify(currentPConfig);
      let pConfigUpdate = Object.assign(currentPConfig, val);
      if (state != JSON.stringify(pConfigUpdate)) {
        this.localStorageService.setJson(LocalStorageService.ARG_PARAMETERS_KEY, pConfigUpdate);
      }
    });
  }

  ngOnDestroy() {
    this.valueChangesSubscription.unsubscribe()
  }
}
