const { v4: uuidv4 } = require('uuid');
const path = require('path');
const fs = require('fs');

// This would be replaced with actual pipeline integration
const pipelineJobs = {};

exports.generateShort = async (req, res) => {
  try {
    const { topic, duration, addCaptions, voiceId } = req.body;
    
    if (!topic) {
      return res.status(400).json({ error: 'Topic is required' });
    }
    
    // Generate a unique ID for this job
    const jobId = uuidv4();
    
    // Create a job entry
    pipelineJobs[jobId] = {
      id: jobId,
      topic,
      duration: duration || 30,
      addCaptions: addCaptions || true,
      voiceId: voiceId || null,
      status: 'queued',
      progress: 0,
      createdAt: new Date(),
      outputPath: null,
      error: null
    };
    
    // Start the pipeline process asynchronously
    processPipelineJob(jobId);
    
    // Return the job ID immediately
    res.status(202).json({ 
      jobId, 
      message: 'Short generation started',
      status: 'queued'
    });
    
  } catch (error) {
    console.error('Error generating short:', error);
    res.status(500).json({ error: 'Failed to generate short' });
  }
};

exports.getStatus = (req, res) => {
  const { id } = req.params;
  
  if (!pipelineJobs[id]) {
    return res.status(404).json({ error: 'Job not found' });
  }
  
  res.status(200).json(pipelineJobs[id]);
};

exports.listShorts = (req, res) => {
  // Convert the jobs object to an array and sort by creation date
  const jobs = Object.values(pipelineJobs).sort((a, b) => 
    new Date(b.createdAt) - new Date(a.createdAt)
  );
  
  res.status(200).json(jobs);
};

exports.downloadShort = (req, res) => {
  const { id } = req.params;
  
  if (!pipelineJobs[id]) {
    return res.status(404).json({ error: 'Job not found' });
  }
  
  const job = pipelineJobs[id];
  
  if (job.status !== 'completed' || !job.outputPath) {
    return res.status(400).json({ error: 'Short is not ready for download' });
  }
  
  const filePath = job.outputPath;
  
  if (!fs.existsSync(filePath)) {
    return res.status(404).json({ error: 'File not found' });
  }
  
  res.download(filePath);
};

// Mock function to simulate pipeline processing
async function processPipelineJob(jobId) {
  const job = pipelineJobs[jobId];
  
  // Update status to processing
  pipelineJobs[jobId] = {
    ...job,
    status: 'processing',
    progress: 10
  };
  
  // Simulate the pipeline steps with timeouts
  
  // Step 1: Generate script
  await new Promise(resolve => setTimeout(resolve, 2000));
  pipelineJobs[jobId].progress = 25;
  
  // Step 2: Generate voiceover
  await new Promise(resolve => setTimeout(resolve, 3000));
  pipelineJobs[jobId].progress = 50;
  
  // Step 3: Generate music
  await new Promise(resolve => setTimeout(resolve, 2000));
  pipelineJobs[jobId].progress = 75;
  
  // Step 4: Generate video and combine everything
  await new Promise(resolve => setTimeout(resolve, 5000));
  
  // Create a mock output file
  const outputDir = path.join(__dirname, '../../public/outputs');
  if (!fs.existsSync(outputDir)) {
    fs.mkdirSync(outputDir, { recursive: true });
  }
  
  const outputPath = path.join(outputDir, `short_${jobId}.mp4`);
  
  // In a real implementation, this would be the actual output file from the pipeline
  // For now, we'll just create an empty file
  fs.writeFileSync(outputPath, '');
  
  // Update job to completed
  pipelineJobs[jobId] = {
    ...pipelineJobs[jobId],
    status: 'completed',
    progress: 100,
    outputPath,
    completedAt: new Date()
  };
}
