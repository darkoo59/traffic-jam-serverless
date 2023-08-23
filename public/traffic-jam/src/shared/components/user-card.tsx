import { User } from "../models/user";
import axios from 'axios';
import Card from "@mui/material/Card";
import CardActions from "@mui/material/CardActions";
import CardContent from "@mui/material/CardContent";
import Typography from "@mui/material/Typography";
import Rating from "@mui/material/Rating";
import { ToastContainer } from "react-toastify";
import { useState } from "react";
import { toast } from "react-toastify";
import {Backdrop, CircularProgress} from '@mui/material'
import { environment } from "../../environments/environment";
import { BackendContext, BackendContextValue } from "../contexts/backend-url-context";
import { useContext } from "react";

export function UserCard({
  user,
  fetchUsers,
}: {
  user: User;
  fetchUsers: () => void;
}) {

  const { url } = useContext<BackendContextValue>(BackendContext);
  const [loading, setLoading] = useState(false);

  interface ErrorResponse {
    errorMessage: string;
  }

  const removeUser = async (email: string | undefined) => { 
  
      setLoading(true)
      axios.get(url+'/delete-user?email='+email)
        .then((response) => {
          // Handle successful response, if needed
          toast.success('User removed successfully');
          fetchUsers()
          setLoading(false)
        })
        .catch((error:any) => {
            setLoading(false)
          if (error.response?.request.status === 405) {
            toast.info("Invalid request method!");
          } else if (error.response?.request.status === 409) {
            toast.error("There isn't users with that email!");
          } else if (error.response?.request.status === 400) {
            toast.error("You aren't provided email!");
          }else {
            toast.error(error.response?.request.message);
          }
        });
  };

  return (
    <div>
    <Card variant="outlined" className="card">
      <ToastContainer />
      <CardContent>
        <Typography sx={{ fontSize: 14 }} color="text.secondary" gutterBottom>
          {user.email}
        </Typography>
        <Typography
          variant="h5"
          component="div"
          className="d-flex justify-content-between align-items-baseline mb-4"
        >
          {user.firstname} {user.lastname}
        </Typography>
        <Typography sx={{ mb: 1.5 }} color="text.secondary">
        <i>Address: </i>
          {user.address}
        </Typography>
        <Typography variant="body2">
          <i>Birthdate: </i>
          {user.birthdate?.toString()}
        </Typography>
        <Typography variant="body2">
          <i>Gender: </i>
          {user.gender}
        </Typography>
        <Typography variant="body2">
          <i>Role: </i>
          {user.role}
        </Typography>
      </CardContent>
        <CardActions className="d-flex align-items-left flex-column">
          <div className="mt-auto">{(
            <div>
                <button
                  type="button"
                  className="btn btn-danger rounded-circle"
                  onClick={() => removeUser(user.email)}
                >
                  Remove
                </button>
              </div>
            )}
          </div>
        </CardActions>
        
    </Card>
    <Backdrop
        sx={{ color: '#fff', zIndex: (theme) => theme.zIndex.drawer + 1 }}
        open={loading}
      >
        <CircularProgress color="inherit" />
      </Backdrop>
    </div>
    
  );
}