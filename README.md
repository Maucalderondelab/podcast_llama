# Create a good LLM story teller


## Improvements of story telling.
As we saw on our first test with the replication of notebook-llama the story is good but not good enough. We aim to develop an advanced story generation system, this means that it should be able to create a coherent story from start to finish.

# ASP and Cot

I’m thinking that the use of a CoT (Chain of Thought) could be more useful than the approach we define above. 

Why? Because we are using ASP as a guidance to achieve a desire output. I think this as a car going to the goal line, the car is the input and the goal is the desire output.

![image.png](https://prod-files-secure.s3.us-west-2.amazonaws.com/3488476f-bfe1-46a3-b593-e9b2319f0f8d/dfab9922-e8dc-4146-9cf0-1fb635e74cd9/image.png)

## What would the ASP represent?

The ASP represent the different routes this car has to obtain this output, some lead to other goal so we think of as roads. when we travel by car we have multiple roads and intersections but out goal line is static, so we use the ASP as an analogy to keep the LLM in “right road” more like a guidance.

![image.png](https://prod-files-secure.s3.us-west-2.amazonaws.com/3488476f-bfe1-46a3-b593-e9b2319f0f8d/cba38ec2-457f-47c9-bacf-dfa06e92491f/image.png)

## What is the CoT in this analogy?

The chain of thought is how our car will go though that road by performing a step by step reasoning, in our task when we have the scene definition and narration (done with the ASP) we can use the SA in combination with the CoT to give the LLM the “ability” to reason step by step to produce the best

![image.png](https://prod-files-secure.s3.us-west-2.amazonaws.com/3488476f-bfe1-46a3-b593-e9b2319f0f8d/7dd31223-2345-4e30-bcba-1e5462f041cc/image.png)