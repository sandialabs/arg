package io.arg.webgui.parts;

import java.io.BufferedReader;
import java.io.File;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URISyntaxException;
import java.net.URL;
import java.nio.file.Paths;
import java.util.Map;
import java.util.Random;

import javax.annotation.PostConstruct;
import javax.annotation.PreDestroy;

import org.eclipse.core.runtime.FileLocator;
import org.eclipse.e4.ui.di.Focus;
import org.eclipse.swt.SWT;
import org.eclipse.swt.chromium.Browser;
import org.eclipse.swt.layout.FillLayout;
import org.eclipse.swt.widgets.Composite;
import org.eclipse.swt.widgets.MessageBox;

/**
 * The ARG web GUI view
 * 
 * @author Didier Verstraete
 *
 */
public class ARGWebGUIView {

	/*
	 * !!! IMPORTANT !!!
	 * 
	 * Currently the Angular client has to be copied into the src/main/resources/api
	 * folder to be launched by the Eclipse plugin.
	 * 
	 * TODO: automatically package the plugin with the flask server and the angular
	 * client with Maven
	 * 
	 * TODO: remove the flask server and Angular client from the src/main/resources
	 * folder
	 */

	// TODO store in config file
	private String apiResourceFolder = "api";
	private File flaskApi = null;

	// TODO store in config file
	private String flaskNgAppPathUrl = "http://127.0.0.1";
	private String flaskShutdownRoute = "/api/v1/server/shutdown";
	
	/**
	 * The system process to launch the flask server
	 */
	private Process apiProcess;

	/**
	 * This browser is the chromium one automatically downloaded with plugin. This
	 * browser is needed to run the latest angular version compatible with ECS6.
	 */
	private Browser browser;
	private int port;
	private String flaskServerAdminKey;

	private static String generateKey(Random random, int length) {
        
		String strAllowedCharacters = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";
        StringBuilder sbRandomString = new StringBuilder(10);
        
        for(int i = 0 ; i < length; i++){
            
            //get random integer between 0 and string length
            int randomInt = random.nextInt(strAllowedCharacters.length());
            
            //get char from randomInt index from string and append in StringBuilder
            sbRandomString.append( strAllowedCharacters.charAt(randomInt) );
        }
        
        return sbRandomString.toString();
        
    }
	
	/**
	 * This method is automatically called when launching the plugin view.
	 * 
	 * @param parent
	 * @throws IOException
	 * @throws URISyntaxException
	 */
	@PostConstruct
	public void createPartControl(Composite parent) throws IOException, URISyntaxException {
		System.out.println("Enter in SampleE4View postConstruct");

		URL fileURL = FileLocator.toFileURL(getClass().getClassLoader().getResource(apiResourceFolder));
		this.flaskApi = Paths.get(new URL(fileURL.toString().replace(" ", "%20")).toURI()).toFile();

		// TODO: need to check the availability of the port before setting it. Multiple
		// local web server can coexists.
		// TODO store default port in config file
		this.port = 5000;

		// start the server providing the API
		this.startArgApi();

		// start the client browser
		browser = new Browser(parent, SWT.BORDER);
		browser.setLayout(new FillLayout());
		browser.setUrl(this.flaskNgAppPathUrl + ":" + this.port);
	}

	/**
	 * This method is automatically called when closing the plugin view.
	 * 
	 * @throws Exception
	 */
	@PreDestroy
	public void cleanUp() throws Exception {
		this.killArgApi();
	}

	/**
	 * Set focus on the browser.
	 */
	@Focus
	public void setFocus() {
		browser.setFocus();
	}

	/**
	 * Starts the flask server in a process and set the server url to the internal
	 * chromium browser.
	 */
	private void startArgApi() {
		try {
			// TODO replace with logger (log4j)
			System.out.println("Starting ARG Api");

			// Constructs the process
			// TODO store in config file
			ProcessBuilder processBuilder = new ProcessBuilder("python", "-m", "flask", "run");

			// set the process arguments for the flask server
			Map<String, String> env = processBuilder.environment();
			env.put("FLASK_APP", flaskApi.toString());
			// TODO store in config file
			env.put("FLASK_DEBUG", "0");
			// TODO store in config file
			// TODO change the server environment to production (in fact needed if server is not local)
			env.put("FLASK_ENV", "development");

			// TODO: need to check the availability of the port before setting it. Multiple
			// local web server can coexists.
			// TODO store default port in config file
			env.put("FLASK_RUN_PORT", String.valueOf(this.port));

			Random rnd = new Random();
			this.flaskServerAdminKey = generateKey(rnd, 10);
			env.put("FLASK_SERVER_ADMIN_KEY", this.flaskServerAdminKey);
			
			processBuilder.redirectErrorStream(true);

			// Starts the process
			apiProcess = processBuilder.start();

		} catch (IOException e1) {
			// TODO manage exception
			e1.printStackTrace();
		}
	}

	/**
	 * Sends to the flask server a stop request to shutdown gracefully
	 * @return
	 * @throws Exception
	 */
	public String requestFlaskServerStop() throws Exception {
      StringBuilder result = new StringBuilder();
      URL url = new URL(this.flaskNgAppPathUrl + ":" + this.port + this.flaskShutdownRoute + "?key=" + this.flaskServerAdminKey);
      HttpURLConnection conn = (HttpURLConnection) url.openConnection();
      conn.setRequestMethod("GET");
      BufferedReader rd = new BufferedReader(new InputStreamReader(conn.getInputStream()));
      String line;
      while ((line = rd.readLine()) != null) {
         result.append(line);
      }
      rd.close();
      return result.toString();
   }
	
	/**
	 * Stops the client and the server
	 */
	private void killArgApi() {

		if (apiProcess != null && apiProcess.isAlive()) {
			// TODO replace with logger (log4j)
			System.out.println("Stopping ARG Api");
			
			
			try
			{
				System.out.println(this.requestFlaskServerStop());			
				apiProcess.wait(10000);
			}
			catch(Exception e) {
				System.err.println(e.getMessage());			
			}
			
			apiProcess.destroy();
			apiProcess = null;
		}

	}

}
