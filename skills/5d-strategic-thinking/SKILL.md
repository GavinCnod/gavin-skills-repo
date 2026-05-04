---
name: 5d-strategic-thinking
description: >
  A high-level strategic analysis tool based on the 5-Dimensional Thinking
  framework (Threads, Levels, Altitude, Perspectives, Time). Use when the user
  presents a complex problem, strategy, or decision-making scenario and needs
  deep, holistic analysis. Trigger phrases: "strategy", "strategic analysis",
  "战略分析", "深度思考", "complex decision", "5D thinking", "holistic analysis",
  "帮我分析战略".
license: MIT
metadata:
  version: "1.0.0"
  author: GavinCnod
  category: strategy-thinking
---

# 5D Strategic Thinking Skill

This skill guides the AI to think like a strategic genius using the 5D framework: Threads, Levels, Altitude, Perspectives (4 Quadrants), and Time.

## Workflow

The process consists of two main phases:
1.  **Phase 1: Interrogation (Information Gathering)**
2.  **Phase 2: 5D Analysis & Strategy (Deep Thinking)**

### Phase 1: Interrogation (The "Ask" Phase)

When the user presents a problem, **DO NOT jump straight to a solution.** Most problems are poorly defined. You must first map the "Missing Territory."

1.  **Scan the 4 Quadrants**: Look at the problem through the lens of the 4 fundamental perspectives (see [framework.md](references/framework.md) Dimension 4 for full definitions). Identify which quadrants are under-represented in the user's description.

2.  **Scan for Time/Context**: What is the history? What is the evolutionary trajectory?

3.  **Generate Questions**: Formulate 3-5 high-impact questions to fill these gaps.
    *   *Example*: "You mentioned the technical failure (Its), but how is the team's morale and trust (We) affecting the response?"
    *   *Example*: "You have the skills (It), but do you truly believe you deserve this success (I)?"

4.  **Output**: Present these questions to the user and ask them to provide context before proceeding to the full analysis.

### Phase 2: 5D Analysis & Strategy (The "Think" Phase)

Once the user provides the context (or if the initial prompt was comprehensive), perform the deep analysis.

**Step 1: Dimension 1 - Threads (Width)**
*   Identify the key domains involved (e.g., Tech, Business, Psychology).
*   Are we missing a crucial discipline? (e.g., trying to solve a psychological problem with engineering).

**Step 2: Dimension 2 - Levels (Depth)**
*   Assess the cognitive level of the situation/actors (see [framework.md](references/framework.md) Dimension 2 for full level definitions).
*   *Strategy*: Ensure the solution is at least one level higher than the problem.

**Step 3: Dimension 3 - Altitude (Balance)**
*   Check for developmental imbalances. Is there high technical competence but low emotional intelligence? Address the "lagging line."

**Step 4: Dimension 4 - Perspectives (4 Quadrants Integration)**
*   Synthesize the data from all 4 quadrants.
*   **Root Cause Analysis**: Is the "system problem" actually a "culture problem"? Is the "behavior problem" actually a "mindset problem"?

**Step 5: Dimension 5 - Time (Evolution)**
*   Apply **Transcend and Include**.
*   Where is this going? What is the next natural evolutionary step?
*   Ensure the strategy doesn't just fix the past, but builds the future.

### Phase 3: Strategic Output

Present the findings in a structured format:
1.  **The Diagnosis**: What is really going on? (Using 5D terms).
2.  **The Gap**: Where is the blockage (Level, Quadrant, or Line)?
3.  **The 5D Strategy**: A step-by-step plan that addresses:
    *   *Mindset (I)*
    *   *Action (It)*
    *   *Culture (We)*
    *   *System (Its)*
4.  **Evolutionary Check**: How this prepares for the long term.

## Examples

**Example 1: Business strategy**
> User: "Our startup is losing market share to a competitor with an inferior product."

Agent enters Phase 1 — scans quadrants, generates questions: "You mentioned the competitor has an inferior product (It), but how is your team's morale (We) and your own confidence in the strategy (I) affecting execution?" Then proceeds to 5D analysis.

**Example 2: Career decision**
> User: "I can't decide whether to take a management role or stay technical."

Agent maps across quadrants (skills, mindset, culture fit, org structure), assesses levels of each option, evaluates evolutionary trajectory, then outputs Diagnosis + Gap + 5D Strategy.

## References

For detailed definitions of all dimensions, refer to [framework.md](references/framework.md).
