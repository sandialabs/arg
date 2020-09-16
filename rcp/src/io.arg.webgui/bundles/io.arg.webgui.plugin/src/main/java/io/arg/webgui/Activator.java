package io.arg.webgui;

import org.osgi.framework.BundleActivator;
import org.osgi.framework.BundleContext;

public class Activator implements BundleActivator {

	private BundleContext context;

	public BundleContext getContext() {
		return context;
	}

	public void start(BundleContext bundleContext) throws Exception {
		context = bundleContext;
	}

	public void stop(BundleContext bundleContext) throws Exception {
		context = null;
	}

}
