// frontend/main.js
const { app, BrowserWindow, ipcMain, dialog } = require('electron');
const path = require('path');
const Store = require('electron-store');

// Initialize store for persistent data
const store = new Store();

let mainWindow;

function createWindow() {
  // Create the browser window
  mainWindow = new BrowserWindow({
    width: 1200,
    height: 800,
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      contextIsolation: true,
      nodeIntegration: false
    }
  });

  // Load the index.html
  mainWindow.loadFile(path.join(__dirname, 'renderer', 'index.html'));

  // Open DevTools in development
  if (process.env.NODE_ENV === 'development') {
    mainWindow.webContents.openDevTools();
  }
}

// Create window when app is ready
app.whenReady().then(() => {
  createWindow();

  app.on('activate', function () {
    if (BrowserWindow.getAllWindows().length === 0) createWindow();
  });
});

// Quit when all windows are closed, except on macOS
app.on('window-all-closed', function () {
  if (process.platform !== 'darwin') app.quit();
});

// IPC handlers
ipcMain.handle('get-token', () => {
  return store.get('token');
});

ipcMain.handle('set-token', (event, token) => {
  store.set('token', token);
  return true;
});

ipcMain.handle('clear-token', () => {
  store.delete('token');
  return true;
});

ipcMain.handle('get-user', () => {
  return store.get('user');
});

ipcMain.handle('set-user', (event, user) => {
  store.set('user', user);
  return true;
});

ipcMain.handle('clear-user', () => {
  store.delete('user');
  return true;
});

ipcMain.handle('select-image', async () => {
  const result = await dialog.showOpenDialog(mainWindow, {
    properties: ['openFile'],
    filters: [
      { name: 'Images', extensions: ['jpg', 'jpeg', 'png', 'gif'] }
    ]
  });

  if (result.canceled) {
    return null;
  }

  return result.filePaths[0];
});