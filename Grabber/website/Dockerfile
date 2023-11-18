# Use an official Node runtime as a parent image
FROM node:14

# Set the working directory to /app
WORKDIR /app

# Copy package.json and package-lock.json to the working directory
COPY package*.json ./

# Install app dependencies
RUN npm install

# Copy the local code into the container at /app
COPY . .

# Build the app
RUN npm run build

# Specify the command to run on container start
CMD ["npm", "run", "serve"]
