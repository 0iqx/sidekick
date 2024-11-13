# Sidekick
Imagine diving into a complex binary file, lines of disassembled code stretch on endlessly.

A common need in binary analysis is getting deeper insights into function behavior and spotting patterns that could improve code quality. Whether you’re reverse engineering, optimizing, or even debugging complex binaries, having tools to help analyze and improve code is invaluable. 

[Binary Ninja’s Sidekick](https://sidekick.binary.ninja/) takes this a step further by using AI to interpret function logic, suggest improvements, and highlight potential issues in real-time. 

# What Sidekick Does?

**Sidekick** is more than just a code viewer, it’s a collaborator. 
Built specifically for **Binary Ninja**, **Sidekick** uses AI to understand what individual functions in a binary actually do. 
This isn’t a simple code review; **Sidekick** identifies patterns, infers behavior, and makes intelligent recommendations for improvements or changes based on the function's purpose.

Here’s how it works:

1. **Function Analysis**: **Sidekick** dives into each function, identifying key elements, loops, calls, and variables. It breaks down the code to give you an analysis that’s more than skin-deep.

2. **Insight Generation**: Based on its analysis, Sidekick offers suggestions on how to optimize or alter the function. Perhaps it will recommend replacing a certain logic with a more efficient one, or it may even spot redundant operations that you can safely remove.

3. **Live Recommendations**: Rather than static insights, Sidekick operates in real-time, meaning you get feedback and suggestions dynamically as you navigate through functions in your binary.

# Sidekick in Action

## Challenge 1: M47H
![image](https://github.com/user-attachments/assets/41768d96-8b66-4bb1-b5a7-5f52b7595476)

I’ll tackle this challenge using only Sidekick, as if I have no prior reverse engineering knowledge.
![image](https://github.com/user-attachments/assets/2c9f4c74-df27-49e4-a6a2-c44f953c5c27)
Let’s have Sidekick analyze the `_start` function to retrieve the flag.

![image](https://github.com/user-attachments/assets/4b195c0d-77e3-4228-af46-cf606e97a0c3)
![image](https://github.com/user-attachments/assets/5e0093d0-8923-4967-9d66-985e5b681c8a)


Without even reading the decompiled code and only using Sidekick, I already know the length and some mathematical operations, like modulus. Now, let’s have Sidekick solve it.

![image](https://github.com/user-attachments/assets/f510d40d-6f34-4c4a-863e-ea79ac22132c)

Before fully solving the challenge, let’s explore another feature: `Suggestions`. This feature allows Sidekick to rename or modify code with more understandable names, based on the user's approval.

![image](https://github.com/user-attachments/assets/48c18e86-249d-475e-b575-00002822e497)


After applying the **Suggestions**, we’ll have a more readable decompiled code, which can improve both our approach to solving the challenge and Sidekick's analysis.

![image](https://github.com/user-attachments/assets/d2b50db1-7bdc-4892-8784-2f3f7868b437)


What if it can take the values from the binary?

![image](https://github.com/user-attachments/assets/a845af67-cd25-4a21-8930-3a9fe8eb4e6a)

Well, it can, but it’s a bit lazy.

![image](https://github.com/user-attachments/assets/b2205c23-1fe5-4925-ac1e-d5b1b204afba)

Sometimes it can correctly take and replace the values, but at least it solves the challenge without any assistance.

![image](https://github.com/user-attachments/assets/4ad2fbda-a04b-41db-b656-6ff861531ffb)

Ah, don’t know how to write code? No problem. Sidekick has you covered!

![image](https://github.com/user-attachments/assets/ec216e82-275b-4707-85a2-d0e8f5cb715c)

Well, we used Sidekick to reverse the binary, write the code, and even fix its errors.
