# Task: Conversational Resume API

Your task is to develop an API that interacts with users conversationally to gather the necessary information for generating a resume. The API should dynamically ask questions and continue the interaction until it has enough details to create a complete resume in either text format for Word Documents and/or PDF.

# Requirements:

- Conversational Interaction: The program should engage with users dynamically, collecting their details as needed.
- Resume Generation: Once enough information is collected, the program should generate a well-structured resume (ideally replicating the format attached).
- API Implementation: The program should be structured as an API, ensuring it can be integrated with other systems.

# Optional Features/Enhancements:

- User Interface (UI):Candidates can develop a basic UI to improve the user experience.

- Voice Integration: Adding voice interaction is optional but will be considered a plus.

# Submission Format and Requirements:

Your reply email should include:

- API Code – The main implementation, including any helper functions.
- Link to Git Hub or attach a ZIP
- Testing Code – A script to test the API’s functionality.
- Link to Git Hub or include in the ZIP
- Video Explanation (3 minutes max) – A brief video explaining the code, demonstrating its functionality, or outlining next steps.
- Link to Google Drive/YouTube (make sure viewing access it open to everyone) or attach an MP4

We recommend spending the first 100 minutes building your API and the final 20 minutes recording your video. It is possible that you may not complete the task comprehensively in the time period, but we care more about your quality of work and thought than a completed project.

# Notes

Got stuck on a bug with the request for a while. I didn't know that FastAPI can only support one body parameter, so the user_input was always blank, and it was stuck on the first question infinitely. Wrapping both values with ConversationRequest class fixed it, but only with 5min remaining so I didn't get to the document generator or demo video. The test script does work to display mostly correct values, theres an issue with populating skills/interests but I didn't get to it.
