import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin
} from '@jupyterlab/application';

import { IThemeManager } from '@jupyterlab/apputils';

/**
 * Initialization data for the JupyterEarthTheme extension.
 */
const plugin: JupyterFrontEndPlugin<void> = {
  id: 'JupyterEarthTheme:plugin',
  description: 'A JupyterLab/Notebook 7 theme.',
  autoStart: true,
  requires: [IThemeManager],
  activate: (app: JupyterFrontEnd, manager: IThemeManager) => {
    console.log('JupyterLab extension JupyterEarthTheme is activated!');
    const style = 'JupyterEarthTheme/index.css';

    manager.register({
      name: 'JupyterEarthTheme',
      isLight: true,
      load: () => manager.loadCSS(style),
      unload: () => Promise.resolve(undefined)
    });
  }
};

export default plugin;
