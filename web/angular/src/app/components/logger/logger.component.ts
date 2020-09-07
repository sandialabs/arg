/**
*HEADER
*         arg/web/angular/src/app/components/logger/logger.component.ts
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
import { Component, OnInit, ViewChild, ElementRef} from '@angular/core';

// Services
import { EventService } from './../../services/event.service';

@Component({
  selector: 'app-logger',
  templateUrl: './logger.component.html',
  styleUrls: ['./logger.component.scss']
})
export class LoggerComponent implements OnInit {
  /**
   * @variables
   */
  public logs: Array<{ date: Date, level: String, message: String }>;
  @ViewChild("loggerContainer", {read: ElementRef}) loggerContainer: ElementRef;

  /**
   * @constructor
   */
  constructor(
    private eventService: EventService
  ) {
    // Init
    this.logs = [];
  }

  /**
   * On component init
   *
   * @return {void}
   */
  ngOnInit(): void {
    // Create event listener
    this.eventService.subscribe('logger',
      (log: any) => {

        console.log(log);

        // Add message to the logger list
        this.logs.push({ date: new Date(), level: log.level, message: log.message });

        // If html element exist
        if (this.loggerContainer) {

          console.log(this.loggerContainer.nativeElement.scrollHeight);
          
          // scroll to bottom
          // timeout enables to let time to the interface to update
          let c = this.loggerContainer.nativeElement;
          setTimeout(function(){   
            c.scroll(0, c.scrollHeight);
          }, 100);
          
        }
      });
  }
  /**
   * Clears the displayed logs
   */
  clear(): void {
    this.logs = []
  }
}
