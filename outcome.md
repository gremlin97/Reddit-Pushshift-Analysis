# Reddit Pushshift Database Analysis

## Summary

**S:** Unearth insights from Reddit.

**T:** Load and analyze the Reddit Pushshift database efficiently to uncover trends.

**A:** Using PSQL:
- Utilized pg_bulkload for efficient loading of 1 million tuples in under 250 seconds with parallelization.
- Implemented constraints including Foreign Keys (FK), Primary Keys (PK), and Composite Keys.
- Identified kindest, harshest, most active, and controversial subreddits.
- Experimented with fragmenting the large database using range and round-robin partitioning schemas.

**R:** 
- **Most Controversial:** Subreddits where the proportion of controversial comments (like/dislike ratio ~ 1) exceeds 1000. Includes topics like politics, AskReddit, announcements, and video games related to Minecraft and YouTubers.
  
- **Most Active:** Subreddits with the highest number of comments and highest scores (upvotes - downvotes).
  
- **Most Harsh:** Subreddits with the lowest average score, often mundane topics or NSFW subreddits that do not evoke strong feelings.
  
- **Most Kindest:** Subreddits with the highest average score, typically focused on feminine topics, women empowerment, and racing.

**Other Insights:**
- Analysis of users with the most karma.
- Examination of subreddits with the most comments and most upvoted/downvoted comments.
- Identification of most active subreddits based on posts per month.
