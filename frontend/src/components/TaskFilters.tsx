import React from "react";
import { Filter, Clock, Flag, Tag, CheckCircle2, Circle } from "lucide-react";
import { FilterOptions } from "@/types/task";

interface TaskFiltersProps {
  filters: FilterOptions;
  onFilterChange: (filters: FilterOptions) => void;
}

const TaskFilters: React.FC<TaskFiltersProps> = ({ filters, onFilterChange }) => {
  const handleStatusChange = (status: "pending" | "completed" | undefined) => {
    onFilterChange({
      ...filters,
      status: filters.status === status ? undefined : status
    });
  };

  const handlePriorityChange = (priority: "LOW" | "MEDIUM" | "HIGH" | undefined) => {
    onFilterChange({
      ...filters,
      priority: filters.priority === priority ? undefined : priority
    });
  };

  return (
    <div className="bg-white p-4 rounded-lg border border-gray-200">
      <div className="flex items-center gap-2 mb-4">
        <Filter className="w-4 h-4 text-gray-500" />
        <h3 className="font-medium text-gray-900">Filters</h3>
      </div>

      <div className="space-y-4">
        {/* Status Filter */}
        <div>
          <h4 className="text-sm font-medium text-gray-700 mb-2">Status</h4>
          <div className="flex gap-2">
            <button
              onClick={() => handleStatusChange("pending")}
              className={`flex items-center gap-1 px-3 py-1.5 text-xs rounded-full ${
                filters.status === "pending"
                  ? "bg-blue-100 text-blue-800"
                  : "bg-gray-100 text-gray-600 hover:bg-gray-200"
              }`}
            >
              <Circle className="w-3 h-3" />
              Pending
            </button>
            <button
              onClick={() => handleStatusChange("completed")}
              className={`flex items-center gap-1 px-3 py-1.5 text-xs rounded-full ${
                filters.status === "completed"
                  ? "bg-green-100 text-green-800"
                  : "bg-gray-100 text-gray-600 hover:bg-gray-200"
              }`}
            >
              <CheckCircle2 className="w-3 h-3" />
              Completed
            </button>
          </div>
        </div>

        {/* Priority Filter */}
        <div>
          <h4 className="text-sm font-medium text-gray-700 mb-2">Priority</h4>
          <div className="flex gap-2">
            <button
              onClick={() => handlePriorityChange("LOW")}
              className={`flex items-center gap-1 px-3 py-1.5 text-xs rounded-full ${
                filters.priority === "LOW"
                  ? "bg-green-100 text-green-800"
                  : "bg-gray-100 text-gray-600 hover:bg-gray-200"
              }`}
            >
              <Flag className="w-3 h-3 fill-green-500" />
              Low
            </button>
            <button
              onClick={() => handlePriorityChange("MEDIUM")}
              className={`flex items-center gap-1 px-3 py-1.5 text-xs rounded-full ${
                filters.priority === "MEDIUM"
                  ? "bg-yellow-100 text-yellow-800"
                  : "bg-gray-100 text-gray-600 hover:bg-gray-200"
              }`}
            >
              <Flag className="w-3 h-3 fill-yellow-500" />
              Medium
            </button>
            <button
              onClick={() => handlePriorityChange("HIGH")}
              className={`flex items-center gap-1 px-3 py-1.5 text-xs rounded-full ${
                filters.priority === "HIGH"
                  ? "bg-red-100 text-red-800"
                  : "bg-gray-100 text-gray-600 hover:bg-gray-200"
              }`}
            >
              <Flag className="w-3 h-3 fill-red-500" />
              High
            </button>
          </div>
        </div>

        {/* Due Date Filter */}
        <div>
          <h4 className="text-sm font-medium text-gray-700 mb-2">Due Date</h4>
          <div className="flex gap-2">
            <button className="px-3 py-1.5 text-xs bg-gray-100 text-gray-600 rounded-full hover:bg-gray-200">
              <Clock className="w-3 h-3 inline mr-1" />
              Overdue
            </button>
            <button className="px-3 py-1.5 text-xs bg-gray-100 text-gray-600 rounded-full hover:bg-gray-200">
              Today
            </button>
            <button className="px-3 py-1.5 text-xs bg-gray-100 text-gray-600 rounded-full hover:bg-gray-200">
              This Week
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default TaskFilters;
