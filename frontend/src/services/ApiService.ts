import {instance as axios} from '../plugins/axios';

class ApiService {
  static async get(url: string) {
    try {
      const response = await axios.get(url);
      return response;
    } catch (error) {
      console.error('Error en GET:', error);
      throw error;
    }
  }

  static async post(url: string, data: object) {
    try {
      const response = await axios.post(url, data);
      return response;
    } catch (error) {
      console.error('Error en POST:', error);
      throw error;
    }
  }

  static async put(url: string, data: object) {
    try {
      const response = await axios.put(url, data);
      return response;
    } catch (error) {
      console.error('Error en PUT:', error);
      throw error;
    }
  }

  static async delete(url: string) {
    try {
      const response = await axios.delete(url);
      return response;
    } catch (error) {
      console.error('Error en DELETE:', error);
      throw error;
    }
  }
}

export default ApiService;