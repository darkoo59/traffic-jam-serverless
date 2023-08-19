interface User {
    id?: string;
    firstname?: string;
    lastname?: string;
    email?: string;
    role?: Role;
    address?: string;
    phone?: string;
    gender?: Sex;
    birthdate?: Date;
  }
  
  interface Client extends User {
  
  }
  
  interface Admin extends User {
  
  }
  
  enum Role {
    CLIENT = 0,
    ADMIN = 1
  }
  
  enum Sex {
    MALE = 0,
    FEMALE = 1
  }
  
  export type { User, Client, Admin, Role, Sex }