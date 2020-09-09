package io.arg.webgui.parts;

import java.io.File;
import java.io.IOException;
import java.net.URISyntaxException;
import java.net.URL;
import java.nio.file.Paths;
import java.util.Map;

import javax.annotation.PostConstruct;
import javax.annotation.PreDestroy;

import org.eclipse.core.runtime.FileLocator;
import org.eclipse.e4.ui.di.Focus;
import org.eclipse.swt.SWT;
import org.eclipse.swt.chromium.Browser;
import org.eclipse.swt.layout.FillLayout;
import org.eclipse.swt.widgets.Composite;

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
	private String apiRelativeLocation = "api";

	private File flaskApiPath = null;

	// TODO store in config file
	private String flaskNgAppPathUrl = "http://127.0.0.1:";

	/**
	 * The system process to launch the server
	 */
	private Process apiProcess;

	/**
	 * This browser is the chromium one automatically downloaded with plugin. This
	 * browser is needed to run the latest angular version compatible with ECS6.
	 */
	private Browser browser;
	private int port;

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

		// TODO: remove the flask server and Angular client from the src/main/resources
		// folder
		URL fileURL = FileLocator.toFileURL(getClass().getClassLoader().getResource(apiRelativeLocation));
		this.flaskApiPath = Paths.get(fileURL.toURI()).toFile();

		// TODO: need to check the availability of the port before setting it. Multiple
		// local web server can coexists.
		// TODO store default port in config file
		this.port = 5000;

		// start the server providing the API
		this.startArgApi();

		// start the client browser
		browser = new Browser(parent, SWT.BORDER);
		browser.setLayout(new FillLayout());
		browser.setUrl(this.flaskNgAppPathUrl + this.port);
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
			env.put("FLASK_APP", flaskApiPath.toString());
			// TODO store in config file
			env.put("FLASK_DEBUG", "1");
			// TODO store in config file
			// TODO change the server environment to production
			env.put("FLASK_ENV", "development");

			// TODO: need to check the availability of the port before setting it. Multiple
			// local web server can coexists.
			// TODO store default port in config file
			env.put("FLASK_RUN_PORT", String.valueOf(this.port));

			processBuilder.redirectErrorStream(true);

			// Starts the process
			apiProcess = processBuilder.start();

		} catch (IOException e1) {
			// TODO manage exception
			e1.printStackTrace();
		}
	}

	/**
	 * Stops the client and the server
	 */
	private void killArgApi() {

		if (apiProcess != null && apiProcess.isAlive()) {
			// TODO replace with logger (log4j)
			System.out.println("Stopping ARG Api");

			// TODO be sure to really kill the flask server on the machine
			apiProcess.destroy();
			apiProcess = null;
		}

	}

}
