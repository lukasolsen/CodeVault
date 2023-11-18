# CodeVault - Grabber

This tool is designed to grab information from the users that launch the python file. It will first start by taking all of the browser data, then moving towards mutliple softwares and then send it towards the API or it will use a offline function which is storing it on the PC. This tool is designed to be used for educational purposes only and should not be used for malicious purposes.

## Features

- Custom User auth along
- Grabs website, discord and network data
- Undetected from Windows Antivirus

## Installation

#### API

```bash
cd Grabber/api
npm install
npm start
```

#### Website

```bash
cd Grabber/website
npm install
npm start
```

#### Client (The grabber itself)

```bash
cd Grabber/client
python main.py
```

## API Reference

#### Check if server is running

```http
  GET /
```

| Parameter      | Type     | Description            |
| :------------- | :------- | :--------------------- |
| `Bearer Token` | `string` | **Required**. User JWT |

### User

#### Get all users

```http
  GET /api/v2/user/users
```

| Parameter      | Type     | Description            |
| :------------- | :------- | :--------------------- |
| `Bearer Token` | `string` | **Required**. User JWT |

#### Get user

```http
  GET /api/v2/user/user/${id}
```

| Parameter      | Type     | Description                       |
| :------------- | :------- | :-------------------------------- |
| `Bearer Token` | `string` | **Required**. User JWT            |
| `id`           | `string` | **Required**. Id of item to fetch |

#### Get current logged in user

```http
  GET /api/v2/user/current_user
```

| Parameter      | Type     | Description            |
| :------------- | :------- | :--------------------- |
| `Bearer Token` | `string` | **Required**. User JWT |

#### Verify JWT Token

```http
  GET /api/v2/user/verify_token
```

| Parameter      | Type     | Description            |
| :------------- | :------- | :--------------------- |
| `Bearer Token` | `string` | **Required**. User JWT |

#### Register User

```http
  GET /api/v2/user/register
```

| Parameter  | Type     | Description             |
| :--------- | :------- | :---------------------- |
| `name`     | `string` | **Required**. User Name |
| `password` | `string` | **Required**. Password  |
| `email`    | `string` | **Required**. Email     |

#### Signin User

```http
  GET /api/v2/user/login
```

| Parameter  | Type     | Description            |
| :--------- | :------- | :--------------------- |
| `password` | `string` | **Required**. Password |
| `email`    | `string` | **Required**. Email    |

### Scan

#### Get all scans

```http
  GET /api/v2/scan/scans
```

| Parameter      | Type     | Description            |
| :------------- | :------- | :--------------------- |
| `Bearer Token` | `string` | **Required**. User JWT |

#### Get scan

```http
  GET /api/v2/scan/scan/${id}
```

| Parameter      | Type     | Description            |
| :------------- | :------- | :--------------------- |
| `Bearer Token` | `string` | **Required**. User JWT |

#### Get scan browsers (PRE)

```http
  GET /api/v2/scan/scan/${id}/attacks/browsers/pre
```

| Parameter      | Type     | Description            |
| :------------- | :------- | :--------------------- |
| `Bearer Token` | `string` | **Required**. User JWT |

#### Get scan browser

```http
  GET /api/v2/scan/scan/${id}/attacks/browser/${browser}/${type}
```

| Parameter      | Type     | Description            |
| :------------- | :------- | :--------------------- |
| `Bearer Token` | `string` | **Required**. User JWT |

#### Get scan network

```http
  GET /api/v2/scan/scan/${id}/attacks/network/${type}
```

| Parameter      | Type     | Description            |
| :------------- | :------- | :--------------------- |
| `Bearer Token` | `string` | **Required**. User JWT |

#### Get scan discord

```http
  GET /api/v2/scan/scan/${id}/attacks/discord/overview
```

| Parameter      | Type     | Description            |
| :------------- | :------- | :--------------------- |
| `Bearer Token` | `string` | **Required**. User JWT |

## License

[MIT](https://choosealicense.com/licenses/mit/)

## Authors

- [@Lukas Olsen](https://www.github.com/lukasolsen)
