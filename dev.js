const { spawn } = require('child_process');
const http = require('http');
const path = require('path');

const PROJECT_PATH = path.resolve(__dirname);
const PORT = 5000;
const URL = 'http://localhost:' + PORT;

console.log('='.repeat(65));
console.log('CIVICLENS AI (NAGRIKNETRA) - DEV SERVER');
console.log('Project Directory Path: ' + PROJECT_PATH);
console.log('Localhost Address:      ' + URL);
console.log('='.repeat(65));

// Check if server is already running on localhost:5000
const req = http.get(URL + '/api/health', (res) => {
    let data = '';
    res.on('data', chunk => data += chunk);
    res.on('end', () => {
        try {
            const json = JSON.parse(data);
            console.log('\n>>> Localhost is ACTIVE and RUNNING WELL! <<<');
            console.log('   * Status:      ' + json.status);
            console.log('   * Service:     ' + json.service);
            console.log('   * AI Engine:   ' + json.ai_engine);
            console.log('   * Version:     ' + json.version);
            console.log('\nOpen your browser at: ' + URL + '\n');
        } catch (e) {
            console.log('\nLocalhost is listening on ' + URL + ' (Status ' + res.statusCode + ')');
        }
    });
});

req.on('error', () => {
    console.log('\nLocalhost is not running yet. Starting Python backend (python app.py)...');
    const py = spawn('python', ['app.py'], {
        cwd: PROJECT_PATH,
        stdio: 'inherit',
        shell: true
    });

    py.on('error', (err) => {
        console.error('Failed to start Python server:', err.message);
    });

    py.on('close', (code) => {
        console.log('Server stopped with exit code: ' + code);
    });
});
