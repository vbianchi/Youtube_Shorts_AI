document.addEventListener('DOMContentLoaded', function() {
    // Duration slider value display
    const durationSlider = document.getElementById('duration');
    const durationValue = document.getElementById('durationValue');
    
    if (durationSlider && durationValue) {
        durationSlider.addEventListener('input', function() {
            durationValue.textContent = this.value + ' seconds';
        });
    }
    
    // Form submission
    const createShortForm = document.getElementById('createShortForm');
    if (createShortForm) {
        createShortForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const topic = document.getElementById('topic').value;
            const duration = document.getElementById('duration').value;
            const addCaptions = document.getElementById('addCaptions').checked;
            const voiceId = document.getElementById('voiceSelect').value;
            
            // Show the status modal
            const jobStatusModal = new bootstrap.Modal(document.getElementById('jobStatusModal'));
            jobStatusModal.show();
            
            // Reset modal state
            document.getElementById('statusSpinner').classList.remove('d-none');
            document.getElementById('statusComplete').classList.add('d-none');
            document.getElementById('statusFooter').classList.add('d-none');
            document.getElementById('statusProgress').style.width = '0%';
            document.getElementById('statusTitle').textContent = 'Processing your short...';
            document.getElementById('statusMessage').textContent = 'This may take a few minutes. Please don\'t close this window.';
            
            // Submit the job to the API
            fetch('/api/shorts/generate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    topic,
                    duration: parseInt(duration),
                    addCaptions,
                    voiceId: voiceId || null
                }),
            })
            .then(response => response.json())
            .then(data => {
                if (data.jobId) {
                    // Start polling for job status
                    pollJobStatus(data.jobId);
                } else {
                    showError('Failed to start job');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                showError('An error occurred while submitting your request');
            });
        });
    }
    
    // Load existing shorts
    loadShorts();
    
    // Poll for job status
    function pollJobStatus(jobId) {
        const statusProgress = document.getElementById('statusProgress');
        const statusTitle = document.getElementById('statusTitle');
        const statusMessage = document.getElementById('statusMessage');
        const statusSpinner = document.getElementById('statusSpinner');
        const statusComplete = document.getElementById('statusComplete');
        const statusFooter = document.getElementById('statusFooter');
        const downloadButton = document.getElementById('downloadButton');
        
        const checkStatus = () => {
            fetch(`/api/shorts/status/${jobId}`)
                .then(response => response.json())
                .then(job => {
                    // Update progress bar
                    statusProgress.style.width = `${job.progress}%`;
                    
                    // Update status message
                    if (job.status === 'queued') {
                        statusTitle.textContent = 'Queued';
                        statusMessage.textContent = 'Your short is in the queue and will be processed soon.';
                    } else if (job.status === 'processing') {
                        statusTitle.textContent = 'Processing';
                        statusMessage.textContent = 'Your short is being generated. This may take a few minutes.';
                    } else if (job.status === 'completed') {
                        statusTitle.textContent = 'Completed!';
                        statusMessage.textContent = 'Your YouTube Short has been successfully generated.';
                        statusSpinner.classList.add('d-none');
                        statusComplete.classList.remove('d-none');
                        statusFooter.classList.remove('d-none');
                        downloadButton.href = `/api/shorts/download/${jobId}`;
                        
                        // Refresh the shorts list
                        loadShorts();
                        return; // Stop polling
                    } else if (job.status === 'failed') {
                        statusTitle.textContent = 'Failed';
                        statusMessage.textContent = job.error || 'An error occurred while generating your short.';
                        statusSpinner.classList.add('d-none');
                        statusFooter.classList.remove('d-none');
                        return; // Stop polling
                    }
                    
                    // Continue polling if not completed or failed
                    setTimeout(checkStatus, 2000);
                })
                .catch(error => {
                    console.error('Error checking status:', error);
                    statusTitle.textContent = 'Error';
                    statusMessage.textContent = 'Failed to check job status. Please try again later.';
                    setTimeout(checkStatus, 5000); // Retry after longer delay
                });
        };
        
        // Start checking status
        checkStatus();
    }
    
    // Load existing shorts
    function loadShorts() {
        const shortsList = document.getElementById('shortsList');
        
        fetch('/api/shorts/list')
            .then(response => response.json())
            .then(jobs => {
                if (jobs.length === 0) {
                    shortsList.innerHTML = `
                        <tr>
                            <td colspan="5" class="text-center py-4">No shorts created yet. <a href="#create">Create your first short!</a></td>
                        </tr>
                    `;
                    return;
                }
                
                shortsList.innerHTML = '';
                jobs.forEach(job => {
                    const createdDate = new Date(job.createdAt).toLocaleString();
                    
                    let statusBadge = '';
                    if (job.status === 'queued') {
                        statusBadge = '<span class="badge bg-secondary">Queued</span>';
                    } else if (job.status === 'processing') {
                        statusBadge = '<span class="badge bg-warning text-dark">Processing</span>';
                    } else if (job.status === 'completed') {
                        statusBadge = '<span class="badge bg-success">Completed</span>';
                    } else if (job.status === 'failed') {
                        statusBadge = '<span class="badge bg-danger">Failed</span>';
                    }
                    
                    let actions = '';
                    if (job.status === 'completed') {
                        actions = `<a href="/api/shorts/download/${job.id}" class="btn btn-sm btn-primary">Download</a>`;
                    } else if (job.status === 'processing' || job.status === 'queued') {
                        actions = `<button class="btn btn-sm btn-secondary" onclick="checkJobStatus('${job.id}')">Check Status</button>`;
                    } else {
                        actions = `<button class="btn btn-sm btn-outline-danger" disabled>Failed</button>`;
                    }
                    
                    const row = document.createElement('tr');
                    row.innerHTML = `
                        <td>${job.topic}</td>
                        <td>${createdDate}</td>
                        <td>${statusBadge}</td>
                        <td>
                            <div class="progress">
                                <div class="progress-bar" role="progressbar" style="width: ${job.progress}%" 
                                    aria-valuenow="${job.progress}" aria-valuemin="0" aria-valuemax="100"></div>
                            </div>
                        </td>
                        <td>${actions}</td>
                    `;
                    shortsList.appendChild(row);
                });
            })
            .catch(error => {
                console.error('Error loading shorts:', error);
                shortsList.innerHTML = `
                    <tr>
                        <td colspan="5" class="text-center py-4 text-danger">Error loading shorts. Please refresh the page.</td>
                    </tr>
                `;
            });
    }
    
    // Make checkJobStatus available globally
    window.checkJobStatus = function(jobId) {
        const jobStatusModal = new bootstrap.Modal(document.getElementById('jobStatusModal'));
        jobStatusModal.show();
        
        // Reset modal state
        document.getElementById('statusSpinner').classList.remove('d-none');
        document.getElementById('statusComplete').classList.add('d-none');
        document.getElementById('statusFooter').classList.add('d-none');
        
        // Start polling
        pollJobStatus(jobId);
    };
    
    // Show error in modal
    function showError(message) {
        const statusTitle = document.getElementById('statusTitle');
        const statusMessage = document.getElementById('statusMessage');
        const statusSpinner = document.getElementById('statusSpinner');
        const statusFooter = document.getElementById('statusFooter');
        
        statusTitle.textContent = 'Error';
        statusMessage.textContent = message;
        statusSpinner.classList.add('d-none');
        statusFooter.classList.remove('d-none');
    }
});
