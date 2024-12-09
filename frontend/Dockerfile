# Use Node.js version 19.9.0 as the base image
FROM node:19.9.0

# Set the working directory inside the container
WORKDIR /app

# Copy package.json and package-lock.json into the container
COPY package*.json ./

# Install npm version 9.7.2 explicitly
RUN npm install -g npm@9.7.2

RUN npm install web-vitals

# Install dependencies
RUN npm install

# Copy the rest of the application code
COPY . .

# Expose port 3000
EXPOSE 3000

# Start the React application
CMD ["npm", "start"]
