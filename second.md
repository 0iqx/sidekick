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

2. **Insight Generation**: Based on its analysis, **Sidekick** offers suggestions on how to optimize or alter the function. Perhaps it will recommend replacing a certain logic with a more efficient one, or it may even spot redundant operations that you can safely remove.

3. **Live Recommendations**: Rather than static insights, **Sidekick** operates in real-time, meaning you get feedback and suggestions dynamically as you navigate through functions in your binary.

# Sidekick in Action

## Challenge 1: M47H - FlagYard
![image](https://github.com/user-attachments/assets/41768d96-8b66-4bb1-b5a7-5f52b7595476)

I’ll tackle this challenge using only **Sidekick**, as if I have no prior reverse engineering knowledge.
![image](https://github.com/user-attachments/assets/2c9f4c74-df27-49e4-a6a2-c44f953c5c27)
Let’s have **Sidekick** analyze the `_start` function to retrieve the flag.

![image](https://github.com/user-attachments/assets/4b195c0d-77e3-4228-af46-cf606e97a0c3)
![image](https://github.com/user-attachments/assets/5e0093d0-8923-4967-9d66-985e5b681c8a)


Without even reading the decompiled code and only using **Sidekick**, I already know the length and some mathematical operations, like modulus. Now, let’s have **Sidekick** solve it.

![image](https://github.com/user-attachments/assets/f510d40d-6f34-4c4a-863e-ea79ac22132c)

Before fully solving the challenge, let’s explore another feature: `Suggestions`. This feature allows **Sidekick** to rename or modify code with more understandable names, based on the user's approval.

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

## Challenge 2: Catbert Ransomware - Flare-On 11
This challenge is quite difficult for Sidekick to solve and will require a lot of questions and nudges. So, I’ll move on to the point where I asked it to analyze the VM and create an enum.

![image](https://github.com/user-attachments/assets/f6d75442-1d84-42bd-87fe-1b269d11fa93)

Well, I think it has identified most of the opcodes correctly. Let’s create the enum.

![image](https://github.com/user-attachments/assets/f05b5056-ab0d-4405-b666-fe9f41744cc1)

I didn’t like the naming, so I’ll ask it to rename it again.

![image](https://github.com/user-attachments/assets/efcad540-f436-468e-858f-bcfab119c567)

Wow! That’s so much better. We can now ask it to write a disassembler, and we’ll be able to view the instructions.

![image](https://github.com/user-attachments/assets/c19ba659-f65a-4cc5-88d2-d6828b20979c)

I had to create another page and adjust it slightly. I think we could get better results if I provided an example of how a VM works.

The [result](https://github.com/0iqx/sidekick/blob/main/sidekickVM.py).

Sidekick was interesting, it generated everything from just a single example of a VM. I used Sidekick while working on this challenge, which inspired me even more to create this post.

The exmple I've used:
```C

#define NEXT_OP()                               \
    (*vm.ip++)
#define NEXT_ARG()                                      \
    ((void)(vm.ip += 2), (vm.ip[-2] << 8) + vm.ip[-1])
#define PEEK_ARG()                              \
    ((vm.ip[0] << 8) + vm.ip[1])
#define POP()                                   \
    (*(--vm.stack_top))
#define PUSH(val)                               \
    (*vm.stack_top = (val), vm.stack_top++)
#define PEEK()                                  \
    (*(vm.stack_top - 1))
#define TOS_PTR()                               \
    (vm.stack_top - 1)


static struct {
    /* Current instruction pointer */
    uint8_t *ip;

    /* Fixed-size stack */
    uint64_t stack[STACK_MAX];
    uint64_t *stack_top;

    /* Operational memory */
    uint64_t memory[MEMORY_SIZE];

    /* A single register containing the result */
    uint64_t result;
} vm;

static void vm_reset(uint8_t *bytecode)
{
    vm = (typeof(vm)) {
        .stack_top = vm.stack,
        .ip = bytecode
    };
}

interpret_result vm_interpret(uint8_t *bytecode)
{
    vm_reset(bytecode);

    for (;;) {
        uint8_t instruction = NEXT_OP();
        switch (instruction) {
        case OP_PUSHI: {
            /* get the argument, push it onto stack */
            uint16_t arg = NEXT_ARG();
            PUSH(arg);
            break;
        }
        case OP_LOADI: {
            /* get the argument, use it to get a value onto stack */
            uint16_t addr = NEXT_ARG();
            uint64_t val = vm.memory[addr];
            PUSH(val);
            break;
        }
        case OP_LOADADDI: {
            /* get the argument, add the value from the address to the top of the stack */
            uint16_t addr = NEXT_ARG();
            uint64_t val = vm.memory[addr];
            *TOS_PTR() += val;
            break;
        }
        case OP_STOREI: {
            /* get the argument, use it to get a value of the stack into a memory cell */
            uint16_t addr = NEXT_ARG();
            uint64_t val = POP();
            vm.memory[addr] = val;
            break;
        }
        case OP_LOAD: {
            /* pop an address, use it to get a value onto stack */
            uint16_t addr = POP();
            uint64_t val = vm.memory[addr];
            PUSH(val);
            break;
        }
        case OP_STORE: {
            /* pop a value, pop an adress, put a value into an address */
            uint64_t val = POP();
            uint16_t addr = POP();
            vm.memory[addr] = val;
            break;
        }

```

Sidekick works best when used wisely. Instead of asking for quick answers like 'Gib me flag,' use it to help with complex problems you’re struggling to understand. Ask it to explain things, and you’ll gain a better understanding. Thanks for reading, and keep cracking!
