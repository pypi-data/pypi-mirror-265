import React, { useContext, useEffect, useRef, useState } from "react";
import profile from "../images/profile.png";
import setting from "../images/setting.png";
import robot from "../images/robot.png";
import chat from "../images/chat.png";
import doc from "../images/doc.png";
import { Link, useNavigate } from "react-router-dom";
import { BiSolidMessageAltDetail } from "react-icons/bi";
import { HiDocumentText } from "react-icons/hi";
import { BsRobot } from "react-icons/bs";
import { FiSettings } from "react-icons/fi";
import { useLocation } from "react-router-dom";
import roleContext from "../contexts/roleContext";

const Sidebar = () => {
  const { pathname } = useLocation();
  const agentContext = useContext(roleContext);
  const menu = agentContext?.agentType?.features;
  const modalRef = useRef(null);
  const [isDropdownOpen, setDropdownOpen] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    document.addEventListener("mousedown", handleClickOutside);

    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
    };
  }, []);

  const handleImageClick = () => {
    navigate("/profile");
    setDropdownOpen(!isDropdownOpen);
  };

  // const handleLogOut = () => {
  //     localStorage.removeItem("komodoUser");
  //     navigate('/');
  //     window.location.reload();
  //     setDropdownOpen(false);
  // }
  const handleClickOutside = (e) => {
    if (modalRef.current && !modalRef.current.contains(e.target)) {
      setDropdownOpen(false);
    }
  };

  return (
    <div className=" bg-darkBg px-5 pt-5 max-w-[68px] min-w-[68px] xl:w-[60px] h-screen flex flex-col justify-between items-center">
      <div className="gap-8 flex flex-col items-center justify-center">
        {pathname !== "/" ? (
          <>
            {menu?.includes("chat") && (
              <>
                {pathname === "/chat" || pathname.includes("/details") ? (
                  <Link to="/chat">
                    {/* <Link
              to="/chat"
              className={`${
                pathname === "/chat" || pathname.includes("/details")
                  ? "bg-[#316FF6] px-2 py-3 rounded-full text-white"
                  : "text-[#C5C8D5]"
              }`}
            > */}
                    <div className="bg-customBgDark p-2.5 rounded-full text-white">
                      <svg
                        xmlns="http://www.w3.org/2000/svg"
                        width="26"
                        height="26"
                        viewBox="0 0 24 18"
                        fill="none"
                      >
                        <path
                          d="M18.5546 0.817871H7.58507C4.95304 0.817871 2.81163 2.78037 2.81163 5.19287V12.8835L0.822569 15.8194C0.733591 15.9506 0.682026 16.1036 0.67341 16.2618C0.664793 16.4201 0.699451 16.5778 0.773662 16.7178C0.847872 16.8579 0.958833 16.9751 1.09463 17.0569C1.23043 17.1386 1.38593 17.1819 1.54444 17.1819H18.5546C21.1866 17.1819 23.328 15.2194 23.328 12.8069V5.19287C23.328 2.78037 21.1866 0.817871 18.5546 0.817871ZM14.1241 12.3108H8.13507C8.01822 12.3143 7.90186 12.2943 7.79288 12.252C7.68391 12.2097 7.58453 12.146 7.50064 12.0646C7.41675 11.9832 7.35006 11.8857 7.30452 11.7781C7.25898 11.6704 7.23551 11.5547 7.23551 11.4378C7.23551 11.3209 7.25898 11.2052 7.30452 11.0975C7.35006 10.9899 7.41675 10.8924 7.50064 10.811C7.58453 10.7296 7.68391 10.6658 7.79288 10.6235C7.90186 10.5812 8.01822 10.5612 8.13507 10.5647H14.1241C14.3512 10.5715 14.5666 10.6665 14.7248 10.8295C14.883 10.9925 14.9714 11.2107 14.9714 11.4378C14.9714 11.6649 14.883 11.8831 14.7248 12.0461C14.5666 12.2091 14.3512 12.304 14.1241 12.3108ZM18.0476 7.4374H8.13507C8.01822 7.4409 7.90186 7.4209 7.79288 7.3786C7.68391 7.3363 7.58453 7.27255 7.50064 7.19113C7.41675 7.10972 7.35006 7.01229 7.30452 6.90463C7.25898 6.79697 7.23551 6.68125 7.23551 6.56435C7.23551 6.44745 7.25898 6.33174 7.30452 6.22408C7.35006 6.11642 7.41675 6.01899 7.50064 5.93758C7.58453 5.85616 7.68391 5.79241 7.79288 5.75011C7.90186 5.70781 8.01822 5.68781 8.13507 5.69131H18.0476C18.2746 5.6981 18.49 5.79306 18.6482 5.95605C18.8064 6.11903 18.8949 6.33723 18.8949 6.56435C18.8949 6.79148 18.8064 7.00968 18.6482 7.17266C18.49 7.33565 18.2746 7.43061 18.0476 7.4374Z"
                          fill="white"
                        />
                      </svg>
                    </div>
                  </Link>
                ) : (
                  <Link
                    to="/chat"
                    className="bg-transparent p-2.5 rounded-full"
                  >
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      width="26"
                      height="26"
                      viewBox="0 0 24 18"
                      fill="none"
                    >
                      <path
                        d="M18.5546 0.817871H7.58507C4.95304 0.817871 2.81163 2.78037 2.81163 5.19287V12.8835L0.822569 15.8194C0.733591 15.9506 0.682026 16.1036 0.67341 16.2618C0.664793 16.4201 0.699451 16.5778 0.773662 16.7178C0.847872 16.8579 0.958833 16.9751 1.09463 17.0569C1.23043 17.1386 1.38593 17.1819 1.54444 17.1819H18.5546C21.1866 17.1819 23.328 15.2194 23.328 12.8069V5.19287C23.328 2.78037 21.1866 0.817871 18.5546 0.817871ZM14.1241 12.3108H8.13507C8.01822 12.3143 7.90186 12.2943 7.79288 12.252C7.68391 12.2097 7.58453 12.146 7.50064 12.0646C7.41675 11.9832 7.35006 11.8857 7.30452 11.7781C7.25898 11.6704 7.23551 11.5547 7.23551 11.4378C7.23551 11.3209 7.25898 11.2052 7.30452 11.0975C7.35006 10.9899 7.41675 10.8924 7.50064 10.811C7.58453 10.7296 7.68391 10.6658 7.79288 10.6235C7.90186 10.5812 8.01822 10.5612 8.13507 10.5647H14.1241C14.3512 10.5715 14.5666 10.6665 14.7248 10.8295C14.883 10.9925 14.9714 11.2107 14.9714 11.4378C14.9714 11.6649 14.883 11.8831 14.7248 12.0461C14.5666 12.2091 14.3512 12.304 14.1241 12.3108ZM18.0476 7.4374H8.13507C8.01822 7.4409 7.90186 7.4209 7.79288 7.3786C7.68391 7.3363 7.58453 7.27255 7.50064 7.19113C7.41675 7.10972 7.35006 7.01229 7.30452 6.90463C7.25898 6.79697 7.23551 6.68125 7.23551 6.56435C7.23551 6.44745 7.25898 6.33174 7.30452 6.22408C7.35006 6.11642 7.41675 6.01899 7.50064 5.93758C7.58453 5.85616 7.68391 5.79241 7.79288 5.75011C7.90186 5.70781 8.01822 5.68781 8.13507 5.69131H18.0476C18.2746 5.6981 18.49 5.79306 18.6482 5.95605C18.8064 6.11903 18.8949 6.33723 18.8949 6.56435C18.8949 6.79148 18.8064 7.00968 18.6482 7.17266C18.49 7.33565 18.2746 7.43061 18.0476 7.4374Z"
                        fill="#C5C8D5"
                      />
                    </svg>
                  </Link>
                )}
              </>
            )}

            {menu?.includes("chatdoc") && (
              <>
                {pathname === "/chatdoc" || pathname.includes("/chatdoc") ? (
                  <Link
                    to="/chatdoc"
                    className="bg-customBgDark p-2.5 rounded-full"
                  >
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      width="26"
                      height="26"
                      viewBox="0 0 29 28"
                      fill="none"
                    >
                      <path
                        fill-rule="evenodd"
                        clip-rule="evenodd"
                        d="M0.5 5.60002C0.5 2.50741 3.00741 0 6.10002 0H22.9001C25.9927 0 28.5001 2.50741 28.5001 5.60002V18.6667C28.5001 21.7593 25.9927 24.2667 22.9001 24.2667H18.1905L15.2024 27.6814C15.1148 27.7814 15.0068 27.8617 14.8857 27.9166C14.7645 27.9716 14.6331 28 14.5 28C14.367 28 14.2356 27.9716 14.1144 27.9166C13.9933 27.8617 13.8853 27.7814 13.7977 27.6814L10.8101 24.2667H6.10002C3.00741 24.2667 0.5 21.7593 0.5 18.6667V5.60002ZM14.5 5.60002C14.7116 5.60003 14.9168 5.67188 15.0821 5.80381C15.2475 5.93574 15.3631 6.11991 15.41 6.32615L15.9266 8.59743C16.0437 9.11208 16.3038 9.58317 16.677 9.95638C17.0502 10.3296 17.5213 10.5897 18.036 10.7068L20.3073 11.2234C20.5135 11.2704 20.6976 11.386 20.8295 11.5513C20.9614 11.7167 21.0332 11.9219 21.0332 12.1334C21.0332 12.3449 20.9614 12.5501 20.8295 12.7154C20.6976 12.8807 20.5135 12.9964 20.3073 13.0434L18.036 13.56C17.5213 13.677 17.0502 13.9371 16.677 14.3104C16.3038 14.6836 16.0437 15.1547 15.9266 15.6693L15.41 17.9401C15.3631 18.1463 15.2474 18.3305 15.0821 18.4623C14.9168 18.5942 14.7115 18.6661 14.5 18.6661C14.2886 18.6661 14.0833 18.5942 13.918 18.4623C13.7527 18.3305 13.637 18.1463 13.59 17.9401L13.0734 15.6693C12.9564 15.1547 12.6963 14.6836 12.3231 14.3104C11.9498 13.9371 11.4788 13.677 10.9641 13.56L8.69329 13.0434C8.48709 12.9964 8.30296 12.8807 8.17107 12.7154C8.03918 12.5501 7.96735 12.3449 7.96735 12.1334C7.96735 11.9219 8.03918 11.7167 8.17107 11.5513C8.30296 11.386 8.48709 11.2704 8.69329 11.2234L10.9641 10.7068C11.4788 10.5897 11.9498 10.3296 12.3231 9.95638C12.6963 9.58317 12.9564 9.11208 13.0734 8.59743L13.59 6.32662C13.6369 6.12029 13.7525 5.93601 13.9178 5.80399C14.0832 5.67197 14.2885 5.60005 14.5 5.60002Z"
                        fill="white"
                      />
                    </svg>
                  </Link>
                ) : (
                  <Link
                    to="/chatdoc"
                    className="bg-transparent p-2.5 rounded-full"
                  >
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      width="26"
                      height="26"
                      viewBox="0 0 29 28"
                      fill="none"
                    >
                      <path
                        fill-rule="evenodd"
                        clip-rule="evenodd"
                        d="M0.5 5.60002C0.5 2.50741 3.00741 0 6.10002 0H22.9001C25.9927 0 28.5001 2.50741 28.5001 5.60002V18.6667C28.5001 21.7593 25.9927 24.2667 22.9001 24.2667H18.1905L15.2024 27.6814C15.1148 27.7814 15.0068 27.8617 14.8857 27.9166C14.7645 27.9716 14.6331 28 14.5 28C14.367 28 14.2356 27.9716 14.1144 27.9166C13.9933 27.8617 13.8853 27.7814 13.7977 27.6814L10.8101 24.2667H6.10002C3.00741 24.2667 0.5 21.7593 0.5 18.6667V5.60002ZM14.5 5.60002C14.7116 5.60003 14.9168 5.67188 15.0821 5.80381C15.2475 5.93574 15.3631 6.11991 15.41 6.32615L15.9266 8.59743C16.0437 9.11208 16.3038 9.58317 16.677 9.95638C17.0502 10.3296 17.5213 10.5897 18.036 10.7068L20.3073 11.2234C20.5135 11.2704 20.6976 11.386 20.8295 11.5513C20.9614 11.7167 21.0332 11.9219 21.0332 12.1334C21.0332 12.3449 20.9614 12.5501 20.8295 12.7154C20.6976 12.8807 20.5135 12.9964 20.3073 13.0434L18.036 13.56C17.5213 13.677 17.0502 13.9371 16.677 14.3104C16.3038 14.6836 16.0437 15.1547 15.9266 15.6693L15.41 17.9401C15.3631 18.1463 15.2474 18.3305 15.0821 18.4623C14.9168 18.5942 14.7115 18.6661 14.5 18.6661C14.2886 18.6661 14.0833 18.5942 13.918 18.4623C13.7527 18.3305 13.637 18.1463 13.59 17.9401L13.0734 15.6693C12.9564 15.1547 12.6963 14.6836 12.3231 14.3104C11.9498 13.9371 11.4788 13.677 10.9641 13.56L8.69329 13.0434C8.48709 12.9964 8.30296 12.8807 8.17107 12.7154C8.03918 12.5501 7.96735 12.3449 7.96735 12.1334C7.96735 11.9219 8.03918 11.7167 8.17107 11.5513C8.30296 11.386 8.48709 11.2704 8.69329 11.2234L10.9641 10.7068C11.4788 10.5897 11.9498 10.3296 12.3231 9.95638C12.6963 9.58317 12.9564 9.11208 13.0734 8.59743L13.59 6.32662C13.6369 6.12029 13.7525 5.93601 13.9178 5.80399C14.0832 5.67197 14.2885 5.60005 14.5 5.60002Z"
                        fill="#C5C8D5"
                      />
                    </svg>
                  </Link>
                )}
              </>
            )}

            {menu?.includes("reportbuilder") && (
              <>
                {pathname === "/document" ? (
                  <Link
                    to="/document"
                    className="bg-customBgDark p-2.5 rounded-full"
                  >
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      width="26"
                      height="26"
                      viewBox="0 0 31 27"
                      fill="none"
                    >
                      <path
                        fill-rule="evenodd"
                        clip-rule="evenodd"
                        d="M6.83325 3C6.83325 2.20435 7.14932 1.44129 7.71193 0.87868C8.27454 0.31607 9.0376 0 9.83325 0H21.8333C22.6289 0 23.392 0.31607 23.9546 0.87868C24.5172 1.44129 24.8333 2.20435 24.8333 3V4.5H6.83325V3ZM3.83325 9.75C3.83325 8.95435 4.14932 8.19129 4.71193 7.62868C5.27454 7.06607 6.0376 6.75 6.83325 6.75H24.8333C25.6289 6.75 26.392 7.06607 26.9546 7.62868C27.5172 8.19129 27.8333 8.95435 27.8333 9.75V11.25H3.83325V9.75ZM0.833252 16.5C0.833252 15.7044 1.14932 14.9413 1.71193 14.3787C2.27454 13.8161 3.0376 13.5 3.83325 13.5H27.8333C28.6289 13.5 29.392 13.8161 29.9546 14.3787C30.5172 14.9413 30.8333 15.7044 30.8333 16.5V21C30.8333 22.5913 30.2011 24.1174 29.0759 25.2426C27.9507 26.3679 26.4246 27 24.8333 27H6.83325C5.24195 27 3.71583 26.3679 2.59061 25.2426C1.46539 24.1174 0.833252 22.5913 0.833252 21V16.5ZM11.7083 18C11.7083 17.7016 11.8268 17.4155 12.0378 17.2045C12.2487 16.9935 12.5349 16.875 12.8333 16.875H18.8333C19.1316 16.875 19.4178 16.9935 19.6287 17.2045C19.8397 17.4155 19.9583 17.7016 19.9583 18C19.9583 18.2984 19.8397 18.5845 19.6287 18.7955C19.4178 19.0065 19.1316 19.125 18.8333 19.125H12.8333C12.5349 19.125 12.2487 19.0065 12.0378 18.7955C11.8268 18.5845 11.7083 18.2984 11.7083 18Z"
                        fill="white"
                      />
                    </svg>
                  </Link>
                ) : (
                  <Link
                    to="/document"
                    className="bg-transparent p-2.5 rounded-full"
                  >
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      width="26"
                      height="26"
                      viewBox="0 0 31 27"
                      fill="none"
                    >
                      <path
                        fill-rule="evenodd"
                        clip-rule="evenodd"
                        d="M6.83325 3C6.83325 2.20435 7.14932 1.44129 7.71193 0.87868C8.27454 0.31607 9.0376 0 9.83325 0H21.8333C22.6289 0 23.392 0.31607 23.9546 0.87868C24.5172 1.44129 24.8333 2.20435 24.8333 3V4.5H6.83325V3ZM3.83325 9.75C3.83325 8.95435 4.14932 8.19129 4.71193 7.62868C5.27454 7.06607 6.0376 6.75 6.83325 6.75H24.8333C25.6289 6.75 26.392 7.06607 26.9546 7.62868C27.5172 8.19129 27.8333 8.95435 27.8333 9.75V11.25H3.83325V9.75ZM0.833252 16.5C0.833252 15.7044 1.14932 14.9413 1.71193 14.3787C2.27454 13.8161 3.0376 13.5 3.83325 13.5H27.8333C28.6289 13.5 29.392 13.8161 29.9546 14.3787C30.5172 14.9413 30.8333 15.7044 30.8333 16.5V21C30.8333 22.5913 30.2011 24.1174 29.0759 25.2426C27.9507 26.3679 26.4246 27 24.8333 27H6.83325C5.24195 27 3.71583 26.3679 2.59061 25.2426C1.46539 24.1174 0.833252 22.5913 0.833252 21V16.5ZM11.7083 18C11.7083 17.7016 11.8268 17.4155 12.0378 17.2045C12.2487 16.9935 12.5349 16.875 12.8333 16.875H18.8333C19.1316 16.875 19.4178 16.9935 19.6287 17.2045C19.8397 17.4155 19.9583 17.7016 19.9583 18C19.9583 18.2984 19.8397 18.5845 19.6287 18.7955C19.4178 19.0065 19.1316 19.125 18.8333 19.125H12.8333C12.5349 19.125 12.2487 19.0065 12.0378 18.7955C11.8268 18.5845 11.7083 18.2984 11.7083 18Z"
                        fill="#C5C8D5"
                      />
                    </svg>
                  </Link>
                )}
              </>
            )}
          </>
        ) : (
          <BiSolidMessageAltDetail className="text-[29px] text-[#797c8c]" />
        )}
      </div>
      <div className="gap-10 flex flex-col items-center mb-5">
        <div onClick={() => navigate("/settings")} className="cursor-pointer">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            width="26"
            height="36"
            viewBox="0 0 29 32"
            fill="none"
          >
            <path
              fill-rule="evenodd"
              clip-rule="evenodd"
              d="M14.3352 10.6294C12.9532 10.6294 11.6279 11.1784 10.6507 12.1556C9.67349 13.1328 9.12451 14.4581 9.12451 15.8401C9.12451 17.222 9.67349 18.5474 10.6507 19.5246C11.6279 20.5018 12.9532 21.0508 14.3352 21.0508C15.7172 21.0508 17.0425 20.5018 18.0197 19.5246C18.9969 18.5474 19.5459 17.222 19.5459 15.8401C19.5459 14.4581 18.9969 13.1328 18.0197 12.1556C17.0425 11.1784 15.7172 10.6294 14.3352 10.6294ZM11.2088 15.8401C11.2088 15.0109 11.5382 14.2157 12.1245 13.6294C12.7108 13.0431 13.506 12.7137 14.3352 12.7137C15.1644 12.7137 15.9596 13.0431 16.5459 13.6294C17.1322 14.2157 17.4616 15.0109 17.4616 15.8401C17.4616 16.6693 17.1322 17.4645 16.5459 18.0508C15.9596 18.6371 15.1644 18.9665 14.3352 18.9665C13.506 18.9665 12.7108 18.6371 12.1245 18.0508C11.5382 17.4645 11.2088 16.6693 11.2088 15.8401Z"
              fill="#C5C8D5"
            />
            <path
              fill-rule="evenodd"
              clip-rule="evenodd"
              d="M19.0803 3.65818C17.7186 -1.1162 10.9517 -1.1162 9.58993 3.65818C9.38671 4.36919 8.91508 4.97338 8.27466 5.34311C7.63424 5.71284 6.87518 5.81917 6.15782 5.63963C1.34037 4.43353 -2.04171 10.2917 1.41263 13.8586C2.48255 14.9633 2.48255 16.7182 1.41263 17.8229C-2.04032 21.3898 1.34176 27.248 6.15643 26.0419C6.87399 25.8619 7.6334 25.9681 8.27414 26.3378C8.91487 26.7076 9.38672 27.312 9.58993 28.0233C10.9517 32.7977 17.7186 32.7977 19.0803 28.0233C19.2835 27.3123 19.7552 26.7081 20.3956 26.3384C21.036 25.9687 21.7951 25.8623 22.5124 26.0419C27.3285 27.248 30.7106 21.3898 27.2576 17.8229C26.7431 17.2914 26.4554 16.5805 26.4554 15.8408C26.4554 15.101 26.7431 14.3902 27.2576 13.8586C30.7106 10.2917 27.3285 4.43353 22.5138 5.63963C21.7963 5.81957 21.0369 5.71345 20.3961 5.34368C19.7554 4.97392 19.2835 4.36949 19.0803 3.65818ZM11.595 4.22927C12.3815 1.47247 16.2888 1.47247 17.0753 4.22927C17.4268 5.46104 18.2435 6.50783 19.3528 7.14832C20.4622 7.78881 21.7771 7.9728 23.0196 7.66137C25.8014 6.96522 27.7551 10.3487 25.7611 12.4093C24.8701 13.3297 24.3719 14.5605 24.3719 15.8415C24.3719 17.1224 24.8701 18.3532 25.7611 19.2736C27.7551 21.3328 25.8014 24.7163 23.0196 24.0201C21.7771 23.7087 20.4622 23.8927 19.3528 24.5332C18.2435 25.1737 17.4268 26.2205 17.0753 27.4522C16.2888 30.209 12.3815 30.209 11.595 27.4522C11.2435 26.2205 10.4267 25.1737 9.31741 24.5332C8.20809 23.8927 6.89316 23.7087 5.65065 24.0201C2.86884 24.7163 0.915179 21.3328 2.90913 19.2736C3.80017 18.3532 4.29835 17.1224 4.29835 15.8415C4.29835 14.5605 3.80017 13.3297 2.90913 12.4093C0.915179 10.3487 2.86884 6.96522 5.65065 7.66137C6.89316 7.9728 8.20809 7.78881 9.31741 7.14832C10.4267 6.50783 11.2435 5.46104 11.595 4.22927Z"
              fill="#C5C8D5"
            />
          </svg>
        </div>

        {pathname !== "/" && (
          <div className="">
            <img
              src={profile}
              alt="profile"
              onClick={handleImageClick}
              className="cursor-pointer"
            />

            {/* {isDropdownOpen && (
                            <div ref={modalRef} className="absolute left-20 bottom-5  bg-white border rounded-md shadow-md text-center">
                                <button className='text-[#5A636C] text-[14px] font-cerebri leading-[30px] px-4 py-[2px] mt-1 cursor-pointer' onClick={handleLogOut}>
                                    Log out
                                </button>
                            </div>
                        )} */}
          </div>
        )}
      </div>
    </div>
  );
};

export default Sidebar;
