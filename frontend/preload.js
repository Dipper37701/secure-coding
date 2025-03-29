// frontend/preload.js
const { contextBridge, ipcRenderer } = require('electron');

// Expose protected methods that allow renderer process to use IPC
contextBridge.exposeInMainWorld('api', {
  // Auth
  getToken: () => ipcRenderer.invoke('get-token'),
  setToken: (token) => ipcRenderer.invoke('set-token', token),
  clearToken: () => ipcRenderer.invoke('clear-token'),
  getUser: () => ipcRenderer.invoke('get-user'),
  setUser: (user) => ipcRenderer.invoke('set-user', user),
  clearUser: () => ipcRenderer.invoke('clear-user'),
  
  // File dialogs
  selectImage: () => ipcRenderer.invoke('select-image')
});

// Debug helper - will print to console when preload script is executed
console.log('Preload script executed. window.api is available now.');